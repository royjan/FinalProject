import sklearn_json as skljson

from SolversInterface import SolversInterface


class ScikitSolver(SolversInterface):
    def train(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)

    def export_to_dict(self) -> dict:
        return skljson.to_dict(self.model)

    def load_from_dict(self, serialized_model: dict):
        self.model = skljson.from_dict(serialized_model)
