from dictalchemy import make_class_dictable
from sqlalchemy import Column, DateTime, String, func, JSON
from sqlalchemy.ext.declarative import declarative_base

from FinalProject.DBManager import DBManager
from FinalProject.Log.Logger import Severity, Logger

Base = declarative_base()
make_class_dictable(Base)


class CeleryTable(Base):
    __tablename__ = "agent"
    group_task_id = Column("group_task_id", String(255), quote=True, primary_key=True)
    status = Column("status", JSON, default={})
    created_date = Column("created_date", DateTime(timezone=True), quote=True, server_default=func.now())
    title = Column("title", String(255), quote=True)
    best_model = Column("best_model", String(255), quote=True)

    @classmethod
    def create_db(cls):
        cls.__table__.create(DBManager.engine)

    def print(self, msg, severity=Severity.DEBUG):
        Logger.print(f'{msg}\nagent_id={str(self.group_task_id)}\n',
                     severity=severity, task_id=self.task_id, task_type='Worker')

    def update_best_model(self, workers):
        from FinalProject.CeleryUtils.CeleryTableWorker import CeleryTableWorker, Statuses
        models_result: [CeleryTableWorker] = [worker for worker in workers if worker.status == Statuses.FINISHED]
        best_model = sorted(models_result, key=lambda model: model.score, reverse=True)[0]
        if best_model:
            self.best_model = best_model.task_id
            DBManager.get_session().merge(self)
            DBManager.get_session().commit()


if __name__ == '__main__':
    CeleryTable.create_db()
