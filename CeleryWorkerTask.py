# from Solvers.SolverInterface import SolverInterface

from FinalProject.DBManager import DBManager
from FinalProject.DataManager import DataManagement
from celery import Celery
from kombu import Queue

broker_url = 'amqp://worker:kingkingking@18.193.6.223:32781/rhost'
backend_url = f'db+postgresql+psycopg2://{DBManager.get_path()}'
app = Celery('CeleryWorkerTask', broker=broker_url, backend=backend_url)

app.conf.task_queues = [Queue('test', durable=True, routing_key='test')]


@app.task
def add(x, y):
    return x + y


@app.task(bind=True)
def test_print(self, *args):
    from FinalProject.CeleryUtils.CeleryTableWorker import CeleryTableWorker
    get_celery_results = CeleryTableWorker.get_workers_by_agent_id(self.id)
    models = [result.model for result in get_celery_results]
    best_model = sorted(models, lambda x: x.score, reverse=True)[0]
    return best_model

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
def train_worker(x, y, config):
    from FinalProject.Solvers.SolverFactory import SolverFactory
    from FinalProject.Solvers.SolversInterface import SolversInterface
    solver: SolversInterface = SolverFactory.get_solver_by_name(config)
    solver.load_from_json(config, y)
    solver.train(x, y)
    score = solver.calculate_auc()
    print(solver.export_to_json())
    return score


if __name__ == '__main__':
    class A:
        pass


    a = A()
    a.y = 7
    b = A()
    b.y = 4
    c = A()
    c.y = 5
    lst = [a, b, c]
    print([x.y for x in sorted(lst, key=lambda x:x.y)])