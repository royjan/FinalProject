from FinalProject.Solvers.SolversInterface import SolversInterface


class ScikitSolver(SolversInterface):
    NAME = "ScikitSolver"

    def __init__(self, model_name):
        self.model_obj = self.get_model_by_name(model_name)()

    @staticmethod
    def get_supported_models():
        from sklearn.linear_model import LinearRegression
        from sklearn.svm import SVC
        from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
        models = {
            "LinearRegression": LinearRegression,
            "SVC": SVC,
            "DecisionTreeClassifier": DecisionTreeClassifier,
            "DecisionTreeRegressor": DecisionTreeRegressor
        }
        return models

    def train(self, X_train, y_train, *args, **kwargs):
        self.model_obj.fit(X_train, y_train, *args, **kwargs)

    def export_to_json(self):
        from sklearn_json import serialize_model
        import json
        return {"class_name": self.NAME, "model": json.dumps(serialize_model(self.model_obj))}

    def load_from_json(self, config, y_train):
        from sklearn_json import deserialize_model
        import json
        model_dict = json.loads(config)
        self.model_obj = deserialize_model(model_dict)

    def export_model_to_file(self):
        import sklearn_json as skljson
        skljson.to_json(self.model_obj, self.get_path())


if __name__ == '__main__':
    z = ScikitSolver("LinearRegression")
    z.train([[1, 2, 3], [4, 5, 6]], [5, 7])
    _dict = z.export_to_json()
    g = ScikitSolver("LinearRegression")
    g.load_from_json(_dict['model'])
    print(g.model_obj.predict([[1, 2, 3]]))
