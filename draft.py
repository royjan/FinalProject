# from DataManager import DataManagement
# from PreprocessData import PreprocessData
#
# if __name__ == '__main__':
#     pp = PreprocessData("data/username.csv", "Username")
#     pp.load_data_from_file()
#     pp.analyze_profile()
#     dm = DataManagement()
#     dm.set_data_from_preprocess_object(pp)
#     dm.df_to_db()
#
# # from DataManager import DataManagement
# from PreprocessData import PreprocessData
#
# if __name__ == '__main__':
#     pp = PreprocessData("data/username.csv", "Username")
#     pp.load_data_from_file()
#     pp.analyze_profile()
#     dm = DataManagement()
#     dm.set_data_from_preprocess_object(pp)
#     dm.df_to_db()
#
#
payload = [
    {"class_name": "ScikitSolver",
     "model_name": "LinearRegression",
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
                        3
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
                      "units": 3,
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
# from DataManager import DataManagement
# from PreprocessData import PreprocessData
#
# if __name__ == '__main__':
#     pp = PreprocessData("data/username.csv", "Username")
#     pp.load_data_from_file()
#     pp.analyze_profile()
#     dm = DataManagement()
#     dm.set_data_from_preprocess_object(pp)
#     dm.df_to_db()
#
#
# from DataManager import DataManagement
# from PreprocessData import PreprocessData
#
# if __name__ == '__main__':
#     pp = PreprocessData("data/username.csv", "Username")
#     pp.load_data_from_file()
#     pp.analyze_profile()
#     dm = DataManagement()
#     dm.set_data_from_preprocess_object(pp)
#     dm.df_to_db()
#
#
from FinalProject.CeleryWorkerTask import train_worker,test_print

group = [train_worker.s(x=[[1, 2, 3], [3, 4, 5], [5, 6, 7]], y=[1, 3, 5], config=_p, agent_id='1') for _p in payload]
from FinalProject.CeleryUtils import CeleryUtils
z = CeleryUtils.create_chords(group, test_print)
z.apply_async(queue='test')
print("asd")