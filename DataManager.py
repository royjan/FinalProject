import os

import pandas as pd
from FinalProject.DBManager import DBManager


class DataManagement:
    LABEL_COLUMN = 'label'

    def __init__(self, title=None, path=None, df=None, label=LABEL_COLUMN):
        self._table = None
        self.title = title
        self.path = path
        self.df = df
        self.label = label

    def set_data_from_preprocess_object(self, preprocess_object):
        self.df = preprocess_object.df
        self.title = preprocess_object.title
        self.path = preprocess_object.path
        self.label = preprocess_object.label

    @property
    def table(self):
        if self._table is None:
            self._table = DBManager.reflect_table(self.table_name)
        return self._table

    def df_to_db(self, delete_local_file=False):
        from FinalProject.DBManager import DBManager
        self.df.rename(columns={self.label: self.LABEL_COLUMN}, inplace=True)
        self.df.to_sql(self.table_name, con=DBManager.engine, index=False, if_exists='replace')
        if delete_local_file:
            for file_name in self.path:
                try:
                    os.remove(file_name)
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

    @property
    def X_train(self):
        from FinalProject.PreprocessData import PreprocessData
        if self.df is None:
            self.db_to_df()
        return self.df[~self.df[PreprocessData.TEST_COLUMN]].drop([self.LABEL_COLUMN, PreprocessData.TEST_COLUMN],
                                                                  axis=1)

    @property
    def y_train(self):
        from FinalProject.PreprocessData import PreprocessData
        if self.df is None:
            self.db_to_df()
        return self.df[~self.df[PreprocessData.TEST_COLUMN]][self.LABEL_COLUMN]

    @property
    def X_test(self):
        from FinalProject.PreprocessData import PreprocessData
        if self.df is None:
            self.db_to_df()
        return self.df[self.df[PreprocessData.TEST_COLUMN]].drop([self.LABEL_COLUMN, PreprocessData.TEST_COLUMN],
                                                                 axis=1)

    @property
    def y_test(self):
        from FinalProject.PreprocessData import PreprocessData
        if self.df is None:
            self.db_to_df()
        return self.df[self.df[PreprocessData.TEST_COLUMN]][self.LABEL_COLUMN]

    @staticmethod
    def delete_table(table_name):
        DBManager.get_session().execute(f'drop table if exists "{table_name}" cascade')
        DBManager.get_session().commit()

    @property
    def table_name(self):
        return f'{self.title}_data'
