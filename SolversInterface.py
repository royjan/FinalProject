class SolversInterface:
    model = None

    def load_from_json(self):
        raise NotImplemented

    def export_to_json(self):
        raise NotImplemented

    def train(self, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def get_path(cls):
        raise NotImplemented
