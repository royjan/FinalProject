import sys
sys.path.append('FinalProject')

class SolversInterface:
    model_obj = None
    NAME = "SolversInterface"
    EXTENSION = "json"

    @classmethod
    def get_solvers(cls):
        return {class_obj.NAME: class_obj for class_obj in cls.__subclasses__()}

    def load_from_json(self, config, y_train):
        raise NotImplementedError

    def export_to_json(self):
        raise NotImplementedError

    def predict(self, X):
        X = X.copy().dropna(how='any')
        return self.model_obj.predict(X)

    @staticmethod
    def calculate_score(y_test, y_pred):
        from sklearn.metrics import roc_auc_score
        return roc_auc_score(y_test, y_pred, multi_class="ovr")

    @staticmethod
    def get_datetime_to_path():
        from datetime import datetime
        return datetime.now().strftime("%d%m%Y_%H%M")

    @classmethod
    def get_model_by_name(cls, model_name):
        models = cls.get_supported_models()
        try:
            return models[model_name]
        except KeyError:
            from FinalProject.Log.Logger import Logger, Severity
            Logger.print(f"{model_name} doesn't define", severity=Severity.ERROR)
            raise ValueError("Model not found please check yourself!")

    @staticmethod
    def get_supported_models():
        raise NotImplementedError

    def export_model_to_file(self):
        import pickle
        with open(self.get_path(), 'wb') as file:
            pickle.dump(self.model_obj, file)

    def train(self, X_train, y_train, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_path(cls):
        return f"{cls.get_datetime_to_path()}_{cls.NAME}.{cls.EXTENSION}"
