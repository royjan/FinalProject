from FinalProject.CeleryUtils.CeleryUtils import group_tasks
from FinalProject.CeleryWorkerTask import train_worker, compare_models
from FinalProject.CeleryUtils import CeleryUtils
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
                        10
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

group = group_tasks(train_worker, payload, 'test')
agent = CeleryUtils.create_chords(group, compare_models, dataset_name='test')
agent.apply_async(queue='test')
