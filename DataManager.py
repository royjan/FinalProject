import os

from DBManager import DBManager
from draft import PreprocessData


class DataManagement:
    def __init__(self, preprocess_object: PreprocessData):
        self.preprocess_object = preprocess_object
        self._table = None

    @property
    def table(self):
        if not self._table:
            self._table = DBManager.reflect_table(self.table_name)
        return self._table

    def upload_to_db(self, delete_local_file=False):
        from DBManager import DBManager
        self.df.to_sql(self.table_name, con=DBManager.engine)
        if delete_local_file:
            try:
                os.remove(self.preprocess_object.path)
            except OSError:
                pass

    @staticmethod
    def delete_table(table_name):
        DBManager.get_session().execute(f'drop table if exists "{table_name}" cascade')
        DBManager.get_session().commit()

    @property
    def table_name(self):
        return f'{self.preprocess_object.title}_data'

    @property
    def df(self):
        return self.preprocess_object.df
