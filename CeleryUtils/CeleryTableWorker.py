from enum import Enum

from dictalchemy import make_class_dictable
from sqlalchemy import Integer, Column, DateTime, String, JSON, func
from sqlalchemy.ext.declarative import declarative_base

from FinalProject.DBManager import DBManager

Base = declarative_base()
make_class_dictable(Base)

class Statuses:
    SUCCESSED = "Successed"
    FAILED = "Failed"
    FINISHED = "Finished"
    STARTED = "Started"


class CeleryTableWorker(Base):
    __tablename__ = "workers"
    task_id = Column("task_id", String(255), quote=True, primary_key=True)
    status = Column("status", String(255), quote=True)
    created_date = Column("created_date", DateTime(timezone=True), quote=True, server_default=func.now())
    agent_id = Column("agent_id", String(255), quote=True, nullable=False)
    model_settings = Column("model_settings", JSON, default={})
    model_results = Column("model_results", JSON, default={})

    @classmethod
    def create_db(cls):
        cls.__table__.create(DBManager.engine)

    @classmethod
    def get_workers_by_agent_id(cls, agent_id):
        return DBManager.get_session().query(cls).filter_by(cls.agent_id == agent_id).all()


if __name__ == '__main__':
    CeleryTableWorker.create_db()
