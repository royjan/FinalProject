from dictalchemy import make_class_dictable
from sqlalchemy import Integer, Column, DateTime, String, func
from sqlalchemy.ext.declarative import declarative_base
import logging
from DBManager import DBManager

Base = declarative_base()
make_class_dictable(Base)


class LogTable(Base):
    __tablename__ = "logs"
    log_id = Column("log_id", Integer, quote=True, autoincrement=True, primary_key=True)
    created_date = Column("created_date", DateTime(timezone=True), quote=True, server_default=func.now())
    severity = Column("severity", String(255), quote=True)  # 10 \ 20 \ 30 \ 40
    trace = Column("trace", String(255), quote=True)
    task_type = Column("task_type", String(255), quote=True)  # agent \ worker
    task_id = Column("task_id", Integer, quote=True)
    msg = Column("msg", String(255), quote=True)

    def __init__(self, msg, trace, severity='Debug'):  # task_type, task_id,
        self.msg = msg
        self.trace = trace
        # self.task_type = task_type
        # self.task_id = task_id
        self.severity = severity

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])

    @classmethod
    def create_db(cls):
        cls.__table__.create(DBManager.engine)

    @classmethod
    def show_rows(cls):
        rows = DBManager.get_session().query(cls).all()
        for row in rows:
            print(row.msg)


if __name__ == '__main__':
    LogTable.__table__.drop()
    LogTable.create_db()
    # LogTable.show_rows()
