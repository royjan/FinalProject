from dictalchemy import make_class_dictable
from sqlalchemy import Integer, Column, DateTime, String, func
from sqlalchemy.ext.declarative import declarative_base

from DBManager import DBManager

Base = declarative_base()
make_class_dictable(Base)


class LogTable(Base):
    __tablename__ = "logs"
    log_id = Column("task_id", Integer, quote=True, autoincrement=True, primary_key=True)
    created_date = Column("created_date", DateTime(timezone=True), quote=True, server_default=func.now())
    severity = Column("severity", Integer, quote=True)  # 10 \ 20 \ 30 \ 40
    content = Column("content", String(255), quote=True)
    task_type = Column("task_type", String(255), quote=True)  # agent \ worker
    task_id = Column("task_id", Integer, quote=True)

    @classmethod
    def create_db(cls):
        cls.__table__.create(DBManager.engine)


if __name__ == '__main__':
    LogTable.create_db()
