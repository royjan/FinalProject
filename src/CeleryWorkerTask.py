import sys
sys.path.append('FinalProject')

from FinalProject.src.CeleryUtils.CeleryTable import CeleryTable
from FinalProject.src.DBManager import DBManager
from FinalProject.src.DataManager import DataManagement
from FinalProject.src.Solvers.SolverFactory import SolverFactory
from FinalProject.src.Solvers.SolversInterface import SolversInterface
from FinalProject.src.CeleryUtils.CeleryTableWorker import CeleryTableWorker, Statuses
from celery import Celery
from kombu import Queue
import pandas as pd
from FinalProject.src.Log.Logger import Severity
from FinalProject.src.mail import send_mail

broker_url = 'amqp://worker:king@18.193.6.223:32781/rhost'
backend_url = f'db+postgresql+psycopg2://{DBManager.get_path()}'
app = Celery('CeleryWorkerTask', broker=broker_url, backend=backend_url)

app.conf.task_queues = [Queue('test', durable=True, routing_key='test')]


@app.task(bind=True)
def compare_models(self, *server_answers, **params):
    """
        report creation - compare between models and sending the report through email
    """
    dataset_name = params.get('dataset_name')
    my_task_id = self.request.id
    result_ids = {response.get('task_id') for arg in server_answers for response in arg}
    workers = CeleryTableWorker.get_workers_by_task_ids(result_ids)
    statuses = {worker.task_id: worker.status for worker in workers}
    agent = CeleryTable(group_task_id=my_task_id, status=statuses, title=dataset_name)
    agent.update_best_model(workers)
    agent.print("Workers are done!")
    create_report(workers, dataset_name)


def create_report(workers: [CeleryTableWorker], dataset_name: str):
    """
    :param workers: workers data
    :param dataset_name: the title of the data
    create the report by workers data and send through email
    """
    file_name_csv = f'report_{dataset_name}.csv'
    df = pd.DataFrame([worker.as_dict() for worker in workers])
    df = df.iloc[df['model_results'].str.get('score').fillna(-1).astype(int).argsort()[::-1]]
    df.to_csv(file_name_csv, index=False)
    body = f"best_model for {dataset_name}: {df.iloc[0].model_settings}"
    send_mail(['royjan2007@gmail.com', 'roybargil@gmail.com'], body, f"Score Report - {dataset_name.capitalize()}",
              file_name_csv, False)


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
    """
        Each worker is fit X,y and store the score.
        Score is JSON for future.. if we want to measure more than AUC score (f1 and etc...)
    """
    my_task_id = self.request.id
    worker = CeleryTableWorker(task_id=my_task_id, status=Statuses.STARTED, model_settings=config)
    worker.update_db()
    worker.print("Celery worker is starting", severity=Severity.DEBUG)
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
        worker.update_db()
        worker.print(f"Worker {config['class_name']} is done", severity=Severity.INFO)
    return {"task_id": worker.task_id}
