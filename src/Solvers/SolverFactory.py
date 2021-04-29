import importlib
import sys
sys.path.append('FinalProject')


class SolverFactory:

    @staticmethod
    def import_subclasses():
        import os
        root_path = "FinalProject/src/Solvers"
        root_path = os.path.join(os.getcwd(), root_path)
        modules = [classname[:-3].replace("/", ".") for classname in os.listdir(root_path) if
                   not classname.startswith("_")]
        for solver in modules:
            if solver not in ['SolverFactory', 'SolversInterface']:
                importlib.import_module(f"FinalProject.src.Solvers.{solver}")

    @classmethod
    def get_solvers(cls) -> dict:
        from FinalProject.src.Solvers.SolversInterface import SolversInterface
        cls.import_subclasses()
        return SolversInterface.get_solvers()

    @classmethod
    def get_solver_by_name(cls, config):
        solvers = cls.get_solvers()
        solver = solvers.get(config['class_name'])
        if solver:
            return solver(config['model_name'])
        raise ValueError(f"for {config['solver_name']} there is no {config['model_name']}")

    @classmethod
    def get_algorithms(cls):
        models = cls.get_solvers()
        result = []
        for model_name, model_object in models.items():
            supported_models = list(model_object.get_supported_models())
            result.extend([f'{model_name}_{supported_model}' for supported_model in supported_models])
        return result

    @classmethod
    def get_algorithm_by_string(cls, str_input):
        config = {}
        solver_name, model_name = str_input.split("_")
        config['class_name'] = solver_name
        config['model_name'] = model_name
        return cls.get_solver_by_name(config)


if __name__ == '__main__':
    x = SolverFactory.get_algorithm_by_string("ScikitSolver_SVC")
    print()
