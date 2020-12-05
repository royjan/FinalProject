from dictalchemy import make_class_dictable
from sqlalchemy import Integer, Column, DateTime, String, func
from sqlalchemy.ext.declarative import declarative_base

from FinalProject.DBManager import DBManager
from FinalProject.Log.Logger import Severity, Logger

Base = declarative_base()
make_class_dictable(Base)


class CeleryTable(Base):
    __tablename__ = "agent"
    group_task_id = Column("group_task_id", String(255), quote=True, primary_key=True)
    status = Column("status", String(255), quote=True)
    created_date = Column("created_date", DateTime(timezone=True), quote=True, server_default=func.now())

    @classmethod
    def create_db(cls):
        cls.__table__.create(DBManager.engine)

    def print(self, msg, severity=Severity.DEBUG):
        Logger.print(f'{msg}\nagent_id={str(self.group_task_id)}\n',
                     severity=severity, task_id=self.task_id, task_type='Worker')


if __name__ == '__main__':
    CeleryTable.create_db()
