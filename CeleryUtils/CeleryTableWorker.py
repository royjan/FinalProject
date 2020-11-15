from enum import Enum

from dictalchemy import make_class_dictable
from sqlalchemy import Integer, Column, DateTime, String, JSON, func
from sqlalchemy.ext.declarative import declarative_base

from FinalProject.DBManager import DBManager

Base = declarative_base()
make_class_dictable(Base)


class Status(Enum):
    WIP = "Work In Progress"
    FAILED = "Failed"
    SUCCESS = "Success"


class CeleryTableWorker(Base):
    __tablename__ = "workers"
    task_id = Column("task_id", Integer, quote=True, autoincrement=True, primary_key=True)
    status = Column("status", String(255), quote=True)
    created_date = Column("created_date", DateTime(timezone=True), quote=True, server_default=func.now())
    agent_id = Column("agent_id", Integer, quote=True, nullable=False)
    model_settings = Column("model_settings", JSON, default={})
    model_results = Column("model_results", JSON, default={})

    @classmethod
    def create_db(cls):
        cls.__table__.create(DBManager.engine)


if __name__ == '__main__':
    CeleryTableWorker.create_db()
