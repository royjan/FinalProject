# from Solvers.SolverInterface import SolverInterface

from celery import Celery
from kombu import Queue
from FinalProject.DBManager import DBManager
from FinalProject.DataManager import DataManagement

broker_url = 'amqp://worker:kingkingking@18.193.6.223:32781/rhost'
app = Celery('CeleryWorkerTask', broker=broker_url)

app.conf.task_queues = [Queue('test', durable=True, routing_key='test')]


@app.task
def add(x, y):
    return x + y


class CeleryWorkerTask:
    def __init__(self):
        self.table = None
        self.dm = None
        self.rows = None
        self.label = None
        self.model = None

    def set_table(self, title):
        self.dm = DataManagement(title)
        self.table = DBManager.reflect_table(self.dm.table_name)

    #
    # @staticmethod
    # def load_model(self, params: dict):
    #     model_class = params.pop("_model_name")
    #     from Solvers.SolverFactory import SolverFactory
    #     solver: SolverInterface = SolverFactory.get_solver_by_name(model_class)
    #     solver.load_

    def get_data(self):
        self.dm.db_to_df()

    @property
    def df(self):
        if self.dm.df is None:
            self.dm.db_to_df()
        return self.dm.df

    @property
    def X(self):
        return self.df.drop(self.label, axis=1)

    @property
    def y(self):
        return self.df[self.label]


@app.task
def train(x, y, config):
    from FinalProject.Solvers.SolverFactory import SolverFactory
    from FinalProject.Solvers.SolversInterface import SolversInterface
    solver: SolversInterface = SolverFactory.get_solver_by_name(config['class_name'])
    solver.load_from_json(config, y)
    solver.train(x, y)
    print(solver.export_to_json())


if __name__ == '__main__':
    app.worker_main(['worker', '-Q test', '--loglevel=INFO'])
