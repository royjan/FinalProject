from typing import Iterable

from dictalchemy import make_class_dictable
from sqlalchemy import Column, DateTime, String, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from FinalProject.Log.Logger import Logger, Severity, TaskType
from FinalProject.DBManager import DBManager

Base = declarative_base()
make_class_dictable(Base)


class Statuses:
    FAILED = "Failed"
    FINISHED = "Finished"
    STARTED = "Started"


class CeleryTableWorker(Base):
    __tablename__ = "workers"
    task_id = Column("task_id", String(255), quote=True, primary_key=True)
    status = Column("status", String(255), quote=True)
    created_date = Column("created_date", DateTime(timezone=True), quote=True, server_default=func.now())
    model_settings = Column("model_settings", JSON, default={})
    model_results = Column("model_results", JSON, default={})

    def as_dict(self):
        from datetime import datetime
        import json
        _dict = {}
        for key, value in self.asdict().items():
            if type(value) is datetime:
                _dict[key] = value.strftime("%d/%m/%Y, %H:%M:%S")
            elif type(value) is dict:
                _dict[key] = json.dumps(value).replace('\\', '').replace('\\', '')
            else:
                _dict[key] = value
        return _dict

    @classmethod
    def create_db(cls):
        cls.__table__.create(DBManager.engine)

    @classmethod
    def get_workers_by_task_ids(cls, task_ids: Iterable):
        return DBManager.get_session().query(cls).filter(cls.task_id.in_(task_ids)).all()

    def print(self, msg, severity=Severity.DEBUG):
        Logger.print(msg, severity=severity, task_id=self.task_id, task_type=TaskType.WORKER)

    @property
    def score(self):
        return self.model_results.get('score', -1)

    def update_db(self):
        DBManager.get_session().merge(self)
        DBManager.get_session().commit()


if __name__ == '__main__':
    CeleryTableWorker.create_db()
