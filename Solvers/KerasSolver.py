import sklearn_json as skljson
from Solvers.SolversInterface import SolversInterface


class KerasSolver(SolversInterface):
    NAME = "KerasSolver"

    @staticmethod
    def get_supported_models():
        import tensorflow as tf
        models = {
            "KerasRegressor": tf.keras.wrappers.scikit_learn.KerasRegressor,
            "KerasClassifier": tf.keras.wrappers.scikit_learn.KerasClassifier
        }
        return models

    def __init__(self, model_name):
        self.generator = None
        self.model_obj = self.get_model_by_name(model_name)

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

    def export_model_to_file(self):
        skljson.to_json(self.model_obj, self.get_path())

    def train(self, train_x, train_y, *args, **kwargs):
        if self.generator:
            return self.model_obj.fit_generator(self.generator.flow(train_x, train_y), *args, **kwargs)
        return self.model_obj.fit(train_x, train_y, *args, **kwargs)

    def export_to_dict(self) -> dict:
        return skljson.to_dict(self.model_obj)

    def load_from_dict(self, serialized_model: dict):
        self.model_obj = skljson.from_dict(serialized_model)

if __name__ == '__main__':
    z = KerasSolver("KerasRegressor")
    z.train([[1,3,4]], [5])