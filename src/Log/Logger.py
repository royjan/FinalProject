import sys
sys.path.append('FinalProject')

from dictalchemy import make_class_dictable
from sqlalchemy import Integer, Column, DateTime, String, func
from sqlalchemy.ext.declarative import declarative_base
from FinalProject.DBManager import DBManager

Base = declarative_base()
make_class_dictable(Base)


class Severity:
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class TaskType:
    WORKER = "Worker"
    AGENT = "Agent"
    WEB = "Web"


class Logger(Base):
    __tablename__ = "logs"
    log_id = Column("log_id", Integer, quote=True, autoincrement=True, primary_key=True)
    created_date = Column("created_date", DateTime(timezone=True), quote=True, server_default=func.now())
    severity = Column("severity", Integer, quote=True)  # 10 \ 20 \ 30 \ 40
    task_type = Column("task_type", String(255), quote=True)  # agent \ worker
    task_id = Column("task_id", String(255), quote=True)
    msg = Column("msg", String(255), quote=True)

    @classmethod
    def print(cls, msg, severity=Severity.DEBUG, task_id=None, task_type=TaskType.WEB):
        msg = str(msg)
        print(f"{severity}: {msg}")
        DBManager.get_session().execute(
            cls.__table__.insert().values(msg=msg, severity=severity, task_id=task_id, task_type=task_type))
        DBManager.get_session().commit()

    @classmethod
    def create_db(cls):
        cls.__table__.create(DBManager.engine)

    @classmethod
    def show_rows(cls):
        rows = DBManager.get_session().query(cls).all()
        for row in rows:
            print(row.msg)


if __name__ == '__main__':
    Logger.create_db()
