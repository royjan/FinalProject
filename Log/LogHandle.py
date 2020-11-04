import logging
import traceback

from DBManager import DBManager
from Log.LogTable import LogTable


class LogHandle(logging.Handler):
    # A very basic logger that commits a LogRecord to the SQL Db
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        print(record)
        if exc:
            trace = traceback.format_exc()
        log = LogTable(
            severity=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'])
        DBManager.get_session().add(log)
        DBManager.get_session().commit()
