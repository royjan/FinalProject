import importlib


class SolverFactory:

    @staticmethod
    def get_solvers() -> dict:
        from Solvers.SolversInterface import SolversInterface
        import os
        modules = [classname[:-3] for classname in os.listdir(os.path.join(os.getcwd())) if not classname.startswith("_")]#, "Solvers"))]
        for solver in modules:
            importlib.import_module(f"Solvers.{solver}")
        return SolversInterface.get_solvers()

    @staticmethod
    def get_solver_by_name(solver_name):
        solvers = SolverFactory.get_solvers()
        solver = solvers.get(solver_name)
        if solver:
            return solver
        raise ValueError(f"{solver_name} does not found!")

