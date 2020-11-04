import sklearn_json as skljson
import tensorflow as tf

from Solvers.SolversInterface import SolversInterface


class KerasSolver(SolversInterface):
    NAME = "KerasSolver"

    def __init__(self):
        self.generator = None

    def build_image_generator(self):
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
        skljson.to_json(self.model, self.get_path())

    def train(self, train_x, train_y, *args, **kwargs):
        if self.generator:
            return self.model.fit_generator(self.generator.flow(train_x, train_y), *args, **kwargs)
        return self.model.fit(train_x, train_y, *args, **kwargs)

    def export_to_dict(self) -> dict:
        return skljson.to_dict(self.model)

    def load_from_dict(self, serialized_model: dict):
        self.model = skljson.from_dict(serialized_model)
