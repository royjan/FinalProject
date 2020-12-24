from FinalProject.CeleryUtils.CeleryTable import CeleryTable
from FinalProject.DBManager import DBManager
from FinalProject.DataManager import DataManagement
from FinalProject.Solvers.SolverFactory import SolverFactory
from FinalProject.Solvers.SolversInterface import SolversInterface
from FinalProject.CeleryUtils.CeleryTableWorker import CeleryTableWorker, Statuses
from celery import Celery
from kombu import Queue
import pandas as pd
from FinalProject.Log.Logger import Severity
from FinalProject.mail import send_mail

broker_url = 'amqp://worker:king@18.193.6.223:32781/rhost'
backend_url = f'db+postgresql+psycopg2://{DBManager.get_path()}'
app = Celery('CeleryWorkerTask', broker=broker_url, backend=backend_url)

app.conf.task_queues = [Queue('test', durable=True, routing_key='test')]


@app.task(bind=True)
def compare_models(self, *server_answers, **params):
    my_task_id = self.request.id
    result_ids = {response.get('task_id') for arg in server_answers for response in arg}
    workers = CeleryTableWorker.get_workers_by_task_ids(result_ids)
    statuses = {worker.task_id: worker.status for worker in workers}
    agent = CeleryTable(group_task_id=my_task_id, status=statuses, title=params.get('dataset_name'))
    agent.update_best_model(workers)
    create_report(workers)


def create_report(workers):
    df = pd.DataFrame([worker.as_dict() for worker in workers])
    df = df.iloc[df['model_results'].str.get('score').fillna(-1).astype(int).argsort()[::-1]]
    df.to_csv("report.csv", index=False)
    body = f"best_model: {df.iloc[0].model_settings}"
    send_mail('royjan2007@gmail.com', body, "Score Report", 'report.csv', False)


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


@app.task(bind=True)
def train_worker(self, config: dict, dataset_name: str):
    my_task_id = self.request.id
    worker = CeleryTableWorker(task_id=my_task_id, status=Statuses.STARTED, model_settings=config)
    DBManager.get_session().merge(worker)
    DBManager.get_session().commit()
    data = DataManagement(title=dataset_name)
    try:
        solver: SolversInterface = SolverFactory.get_solver_by_name(config)
        solver.load_from_json(config, data.y_train)
        solver.train(data.X_train, data.y_train)
        y_pred = solver.predict(data.X_test)
        score = solver.calculate_score(data.y_test, y_pred)
        worker.model_results = {"score": score}
        worker.status = Statuses.FINISHED
    except Exception as ex:
        worker.status = Statuses.FAILED
        worker.print(repr(ex), Severity.ERROR)
    finally:
        DBManager.get_session().merge(worker)
        DBManager.get_session().commit()
    return {"task_id": worker.task_id}
