import sklearn_json as skljson

from Solvers.SolversInterface import SolversInterface


class ScikitSolver(SolversInterface):
    NAME = "ScikitSolver"

    def train(self, train_x, train_y, *args, **kwargs):
        self.model.fit(train_x, train_y, *args, **kwargs)

    def export_to_dict(self) -> dict:
        return skljson.to_dict(self.model)

    def load_from_dict(self, serialized_model: dict):
        self.model = skljson.from_dict(serialized_model)

    def export_model_to_file(self):
        skljson.to_json(self.model, self.get_path())


