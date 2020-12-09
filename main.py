from FinalProject.CeleryUtils.CeleryUtils import group_tasks
from FinalProject.CeleryWorkerTask import train_worker, compare_models
from FinalProject.CeleryUtils import CeleryUtils
from flask import Flask, render_template

from FinalProject.DBManager import DBManager

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
    import os
    from flask import request
    file_names = []
    for file in request.files.getlist('files[]'):
        file_path = os.path.join('data', file.filename)
        file.save(file_path)
        file_names.append(file_path)
    return file_names


@app.route('/upload', methods=['POST'])
def upload():
    def get_columns_name(title):
        table = DBManager.reflect_table(f'{title}_data')
        return [str(column.key) for column in table.c if str(column.key) != PreprocessData.TEST_COLUMN]

    from flask import request, session
    from FinalProject.PreprocessData import PreprocessData
    from FinalProject.DataManager import DataManagement
    file_names = ['data/train.csv', 'data/test.csv']  # save_and_get_file_names()
    title = session['title'] = request.form['title']
    pp = PreprocessData(path=file_names, title=title)
    pp.set_data()
    data = DataManagement()
    data.set_data_from_preprocess_object(pp)
    data.df_to_db()
    return render_template('preprocess.html', columns=get_columns_name(title))


@app.route('/preprocess', methods=['GET'])
def preprocess():
    from flask import session
    from FinalProject.PreprocessData import PreprocessData
    from FinalProject.DataManager import DataManagement
    pp = PreprocessData(label=session['label'], title=session['title'])
    data = DataManagement()
    data.set_data_from_preprocess_object(pp)
    pp.df = data.db_to_df()
    pp.df = pp.delete_column(pp.df, ['PassengerId', 'Name', 'Cabin', 'Ticket'])
    pp.one_hot_encode()
    pp_settings = None  # PreprocessData.PreprocessDataSettings({'Age': 'median'})
    pp.df = pp.impute(pp_settings)
    pp.apply_smote()
    pp.filter_features('median')
    data.df_to_db(replace_label=True)


@app.route('/train', methods=['GET'])
def train():
    group = group_tasks(train_worker, payload, 'titanic')
    agent = CeleryUtils.create_chords(group, compare_models, dataset_name='titanic')
    agent.apply_async(queue='test')


if __name__ == '__main__':
    app.run()
