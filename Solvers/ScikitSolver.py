from FinalProject.Solvers.SolversInterface import SolversInterface


class ScikitSolver(SolversInterface):
    NAME = "ScikitSolver"

    def __init__(self, model_name):
        self.model_obj = self.get_model_by_name(model_name)()

    @staticmethod
    def get_supported_models():
        from sklearn.linear_model import LinearRegression
        from sklearn.linear_model import LogisticRegression
        from sklearn.svm import SVC
        from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
        models = {
            "LinearRegression": LinearRegression,
            "SVC": SVC,
            "DecisionTreeClassifier": DecisionTreeClassifier,
            "DecisionTreeRegressor": DecisionTreeRegressor,
            "LogisticRegression": LogisticRegression
        }
        return models

    def train(self, X_train, y_train, *args, **kwargs):
        self.model_obj.fit(X_train, y_train, *args, **kwargs)

    def export_to_json(self):
        from sklearn_json import serialize_model
        import json
        return {"class_name": self.NAME, "model": json.dumps(serialize_model(self.model_obj))}

    def load_from_json(self, config, y_train):
        import json
        model_dict = json.loads(config['model'])
        for key, value in model_dict.items():
            setattr(self.model_obj, key, value)

    def export_model_to_file(self):
        import sklearn_json as skljson
        skljson.to_json(self.model_obj, self.get_path())
