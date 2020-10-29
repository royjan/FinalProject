from DataManager import DataManagement
from PreprocessData import PreprocessData
from SolversInterface import SolversInterface


class ScikitSolver(SolversInterface):
    # implement load_from_file, train and etc...
    pass


class KerasSolver(SolversInterface):
    # implement load_from_file, train and etc...
    pass


class TorchSolver(SolversInterface):
    # implement load_from_file, train and etc...
    pass


if __name__ == '__main__':
    pp = PreprocessData("data/username.csv", "Username")
    pp.load_data_from_file()
    pp.analyze_profile()
    dm = DataManagement(pp)
    dm.upload_to_db()


class CeleryTable:
    # group_task_id: int, status: {WIP, FAILED, SUCCESS}, created_date: datetime, sub_task_ids: [int],
    # best_model: string (path), AUC score: float
    pass


class CeleryWorkerTable:
    # task_id: int, status: {WIP, FAILED, SUCCESS}, created_date: datetime, parent_id: int, model_settings: json,
    # AUC score: float
    pass
