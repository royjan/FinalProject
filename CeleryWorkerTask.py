# from Solvers.SolverInterface import SolverInterface

from celery import Celery
from kombu import Queue

from DBManager import DBManager
from DataManager import DataManagement

broker_url = 'amqp://worker:kingkingking@18.193.6.223:32781/rhost'
app = Celery('CeleryWorkerTask', broker=broker_url)

app.conf.task_queues = [Queue('test-q', durable=False, routing_key='test-q')]


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
def multi(x, y):
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    # model.fit(x, y)
    from sklearn_json import to_dict
    print(to_dict(model))


if __name__ == '__main__':
    z = multi.s(x=[[1, 2, 3], [3, 4, 5], [5, 6, 7]], y=[1,3,5]).apply_async(queue='test-q')
    print(z)
