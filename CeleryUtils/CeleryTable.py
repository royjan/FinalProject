from enum import Enum

from dictalchemy import make_class_dictable
from sqlalchemy import Integer, Column, DateTime, String, func
from sqlalchemy.ext.declarative import declarative_base

from FinalProject.DBManager import DBManager

Base = declarative_base()
make_class_dictable(Base)


class Status(Enum):
    WIP = "WORK_IN_PROGRESS"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


class CeleryTable(Base):
    __tablename__ = "agent"
    group_task_id = Column("group_task_id", String(255), quote=True, primary_key=True)
    status = Column("status", String(255), quote=True)
    created_date = Column("created_date", DateTime(timezone=True), quote=True, server_default=func.now())

    @classmethod
    def create_db(cls):
        cls.__table__.create(DBManager.engine)


if __name__ == '__main__':
    CeleryTable.create_db()
