import os

import pandas as pd

from DBManager import DBManager
from PreprocessData import PreprocessData


class DataManagement:
    def __init__(self, title=None, path=None, df=None):
        self._table = None
        self.title = title
        self.path = path
        self.df = df

    def set_data_from_preprocess_object(self, preprocess_object: PreprocessData):
        self.df = preprocess_object.df
        self.title = preprocess_object.title
        self.path = preprocess_object.path

    @property
    def table(self):
        if self._table is None:
            self._table = DBManager.reflect_table(self.table_name)
        return self._table

    def df_to_db(self, delete_local_file=False):
        from DBManager import DBManager
        self.df.to_sql(self.table_name, con=DBManager.engine)
        if delete_local_file:
            try:
                os.remove(self.path)
            except OSError:
                pass

    def get_rows(self, sub_query=False):
        query = DBManager.get_session().query(self.table)
        if sub_query:
            return query
        return query.all()

    def db_to_df(self):
        df = pd.read_sql(self.get_rows(sub_query=True).statement, DBManager.get_session().bind)
        self.df = df

    @staticmethod
    def delete_table(table_name):
        DBManager.get_session().execute(f'drop table if exists "{table_name}" cascade')
        DBManager.get_session().commit()

    @property
    def table_name(self):
        return f'{self.title}_data'
