import os

from DBManager import DBManager
from draft import PreprocessData


class DataManagement:
    def __init__(self, preprocess_object: PreprocessData):
        self.preprocess_object = preprocess_object

    def upload_to_db(self, delete_local_file=False):
        from DBManager import DBManager
        self.df.to_sql(f'{self.preprocess_object.title}_data', con=DBManager.engine)
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
    def df(self):
        return self.preprocess_object.df
