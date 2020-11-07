from Solvers.SolversInterface import SolversInterface


class ScikitSolver(SolversInterface):
    NAME = "ScikitSolver"

    def __init__(self, model_name):
        self.model_obj = self.get_model_by_name(model_name)

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

    def train(self, train_x, train_y, *args, **kwargs):
        self.model.fit(train_x, train_y, *args, **kwargs)

    def export_to_dict(self) -> dict:
        import sklearn_json as skljson
        return {"class_name": self.NAME, "model": skljson.to_dict(self.model)}

    def load_from_dict(self, serialized_model: dict):
        import sklearn_json as skljson
        self.model = skljson.from_dict(serialized_model['model'])

    def export_model_to_file(self):
        import sklearn_json as skljson
        skljson.to_json(self.model, self.get_path())


if __name__ == '__main__':
    import sklearn

    z = sklearn.linear_model.LinearRegression(normalize=True)
    z.fit([[1, 2, 3], [4, 5, 6]], [5, 7])
    ScikitSolver.model = z
    _dict = ScikitSolver().export_to_dict()
    g = ScikitSolver()
    g.load_from_dict(_dict)
    print(g.model.predict([[1, 2, 3]]))
