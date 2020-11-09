from FinalProject.Solvers.SolversInterface import SolversInterface


class KerasSolver(SolversInterface):
    NAME = "KerasSolver"

    @staticmethod
    def get_supported_models():
        models = {
            "Keras": None,
        }
        return models

    def __init__(self, model_name):
        self.generator = None
        self.optimizer_info = {'loss': 'binary_crossentropy', 'optimizer': 'adam', 'metrics': 'accuracy'}

    def build_image_generator(self):
        import tensorflow as tf
        self.generator = tf.keras.preprocessing.image.ImageDataGenerator(
            featurewise_center=False,
            samplewise_center=False,
            featurewise_std_normalization=False,
            samplewise_std_normalization=False,
            zca_whitening=False,
            zca_epsilon=1e-06,
            rotation_range=0,
            width_shift_range=0.0,
            height_shift_range=0.0,
            brightness_range=None,
            shear_range=0.0,
            zoom_range=0.0,
            channel_shift_range=0.0,
            fill_mode="nearest",
            cval=0.0,
            horizontal_flip=False,
            vertical_flip=False,
            rescale=None,
            preprocessing_function=None,
            data_format=None,
            validation_split=0.0,
            dtype=None,
        )

    def train(self, X_train, y_train, *args, **kwargs):
        if self.generator:
            return self.model_obj.fit_generator(self.generator.flow(X_train, y_train), *args, **kwargs)
        return self.model_obj.fit(X_train, y_train, epochs=1000)

    def export_to_json(self):
        return {"class_name": self.NAME, "model": self.model_obj.model.to_json(),
                "optimizer": self.optimizer_info}

    def load_from_json(self, config, y_train):
        import tensorflow
        model = tensorflow.keras.models.model_from_json(config['model'])
        model.compile(**self.get_optimize_settings(config, y_train))
        self.model_obj = model

    def get_optimize_settings(self, config, y) -> dict:
        self.optimizer_info['loss'] = config.get('loss') or 'binary_crossentropy' if \
            len(set(y)) > 2 else 'categorical_crossentropy'
        self.optimizer_info['optimizer'] = config.get("optimizer") or self.optimizer_info['optimizer']
        self.optimizer_info['metrics'] = config.get("metrics") or self.optimizer_info['metrics']
        return self.optimizer_info

    def predict(self, X):
        return self.model_obj.predict(X)


if __name__ == '__main__':
    config = dict()
    config['optimizer'] = {}
    config['model'] = """{
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
              "ragged": false,
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
              "units": 64,
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
    """
    z = KerasSolver()
    z.load_from_json(config, [1])
    z.train([[2, 4, 4]], [1])
    print(z.predict([[2, 4, 4]]))
