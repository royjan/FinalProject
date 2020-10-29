class SolversInterface:
    def load_from_file(self):
        pass

    def export_model(self):
        pass

    def train(self, *args, **kwargs):
        pass

    @classmethod
    def get_path(cls):
        pass