import sys
from flask import Flask, render_template, request, session
import os
import threading

sys.path.append('FinalProject')

from celery.result import AsyncResult
from FinalProject.DBManager import DBManager
from FinalProject.Log.Logger import Logger
from FinalProject.CeleryUtils.CeleryUtils import group_tasks
from FinalProject.CeleryWorkerTask import train_worker, compare_models
from FinalProject.CeleryUtils import CeleryUtils
from FinalProject.PreprocessData import PreprocessData
from FinalProject.DataManager import DataManagement
from FinalProject.Solvers.SolverFactory import SolverFactory

payload = [
    {"class_name": "ScikitSolver",
     "model_name": "LogisticRegression",
     "model": '{"n_jobs":-1}'},
    {"class_name": "KerasSolver", "model_name": "", "model":
        """{
              "class_name": "Sequential",
              "config": {
                "name": "sequential",
                "layers": [
                  {
                    "class_name": "InputLayer",
                    "config": {
                      "batch_input_shape": [
                        null,
                        5
                      ],
                      "dtype": "float32",
                      "sparse": false,
                      "name": "dense_input"
                    }
                  },
                  {
                    "class_name": "Dense",
                    "config": {
                      "name": "dense",
                      "trainable": true,
                      "batch_input_shape": [
                        null,
                        3
                      ],
                      "dtype": "float32",
                      "units": 11,
                      "activation": "relu",
                      "use_bias": true,
                      "kernel_initializer": {
                        "class_name": "GlorotUniform",
                        "config": {
                          "seed": null
                        }
                      },
                      "bias_initializer": {
                        "class_name": "Zeros",
                        "config": {}
                      },
                      "kernel_regularizer": null,
                      "bias_regularizer": null,
                      "activity_regularizer": null,
                      "kernel_constraint": null,
                      "bias_constraint": null
                    }
                  },
                  {
                    "class_name": "Dense",
                    "config": {
                      "name": "dense_2",
                      "trainable": true,
                      "dtype": "float32",
                      "units": 1,
                      "activation": "sigmoid",
                      "use_bias": true,
                      "kernel_initializer": {
                        "class_name": "GlorotUniform",
                        "config": {
                          "seed": null
                        }
                      },
                      "bias_initializer": {
                        "class_name": "Zeros",
                        "config": {}
                      },
                      "kernel_regularizer": null,
                      "bias_regularizer": null,
                      "activity_regularizer": null,
                      "kernel_constraint": null,
                      "bias_constraint": null
                    }
                  }
                ]
              },
              "keras_version": "2.4.0",
              "backend": "tensorflow"
            }
            """}]
app = Flask(__name__)

app.config.update(DEBUG=True, SECRET_KEY='royroy')


@app.route('/')
def index():
    return render_template('index.html')


def save_and_get_file_names():
    train_file = request.files['train_file']
    test_file = request.files.get('test_file')
    uploaded_files = [file_name for file_name in {train_file, test_file} if file_name.filename]
    file_names = []
    for file in uploaded_files:
        file_path = os.path.join('data', file.filename)
        file.save(file_path)
        file_names.append(file_path)
    return file_names


@app.route('/upload', methods=['POST'])
def upload():
    """
        upload files to database and create a report
    """
    def get_columns_name(_title):
        table = DBManager.reflect_table(f'{_title}_data')
        return [str(column.key) for column in table.c if str(column.key) != PreprocessData.TEST_COLUMN]

    file_names = save_and_get_file_names()
    title = session['title'] = request.form['title']
    pp = PreprocessData(path=file_names, title=title)
    pp.set_data()
    analyzer = threading.Thread(target=pp.analyze_profile)
    analyzer.start()
    data = DataManagement()
    data.set_data_from_preprocess_object(pp)
    upload_data = threading.Thread(target=data.df_to_db)
    upload_data.start()
    analyzer.join()
    upload_data.join()
    return render_template('preprocess.html', columns=get_columns_name(title))


@app.route('/preprocess', methods=['POST'])
def preprocess():
    """
        preprocess the data:
        # split train test if only train set uploaded
        # impute to NaN values
        # SMOTE for balance classes
        # filter features by correlation to label
        # OHE for categorical data
        upload to database
    """
    pp = PreprocessData(label=request.form['label'], title=session['title'])
    data = DataManagement()
    data.set_data_from_preprocess_object(pp)
    pp.df = data.db_to_df()
    pp.split_train_test()
    pp.df = pp.delete_column(pp.df, request.form.getlist('dropColumns'))
    impute_method = None if request.form['impute'] == 'None' else request.form['impute']
    pp_settings = PreprocessData.PreprocessDataSettings(impute_method)
    pp.df = pp.impute(pp_settings)
    if request.form.get('smote', 'off') == 'on':
        pp.apply_smote()
    pp.filter_features(request.form['filterFeatures'])
    pp.one_hot_encode()
    data.df = pp.df
    data.df_to_db(replace_label=True)
    Logger.print("Uploaded done successfully")
    return render_template('algorithms.html', algorithms=SolverFactory.get_algorithms())


def parsing_request():
    """
        each pair (model and params) is parsed to dictionaries
    """
    payloads = []
    for num in range(len(request.form) // 2):
        _payload = {}
        algorithm_name = request.form[f'algo_name[new{num}]']
        algorithm_params = request.form[f'algo_params[new{num}]']
        _payload['model'] = algorithm_params
        _payload['class_name'], _payload['model_name'] = algorithm_name.split('_')
        payloads.append(_payload)
    return payloads


@app.route('/get_celery_status', methods=['POST'])
def get_celery_status():
    """
        nice to have: what is the progress of my celery task
    """
    state = None
    try:
        task_id = request.args.get('task_id') or request.json.get('task_id')
        task = AsyncResult(task_id)
        state = task.state
    except Exception as ex:
        pass
    finally:
        return {"status": state}


@app.route('/train', methods=['POST'])
def train():
    """
        create multiple tasks by single tasks and callback with report creation
    """
    from flask import session
    payload = parsing_request()
    group = group_tasks(train_worker, payload, session['title'])
    agent = CeleryUtils.create_chords(group, compare_models, dataset_name=session['title'])
    agent.apply_async(queue='test')
    return {"mission": "Started"}


if __name__ == '__main__':
    app.run()
