class SolversInterface:
    model = None
    NAME = "SolversInterface"
    EXTENSION = "json"

    @classmethod
    def get_solvers(cls):
        return {class_obj.NAME: class_obj for class_obj in cls.__subclasses__()}

    @staticmethod
    def get_datetime_to_path():
        from datetime import datetime
        return datetime.now().strftime("%d%m%Y_%H%M")

    def load_from_json(self):
        raise NotImplemented

    def export_to_json(self):
        raise NotImplemented

    def export_model_to_file(self):
        raise NotImplemented

    def train(self, train_x, train_y, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def get_path(cls):
        return f"{cls.get_datetime_to_path()}_{cls.NAME}.{cls.EXTENSION}"
