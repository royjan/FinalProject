import importlib


class SolverFactory:

    @staticmethod
    def get_solvers() -> dict:
        from FinalProject.Solvers.SolversInterface import SolversInterface
        import os
        modules = [classname[:-3] for classname in os.listdir(os.path.join(os.getcwd(), "FinalProject/Solvers")) if
                   not classname.startswith("_")]
        for solver in modules:
            if solver not in ['SolverFactory', 'SolversInterface']:
                importlib.import_module(f"FinalProject.Solvers.{solver}")
        return SolversInterface.get_solvers()

    @staticmethod
    def get_solver_by_name(config):
        solvers = SolverFactory.get_solvers()
        solver = solvers.get(config['class_name'])
        if solver:
            return solver(config['model_name'])
        raise ValueError(f"for {config['solver_name']} there is no {config['model_name']}")
