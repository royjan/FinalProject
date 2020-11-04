from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBManager:
    user_name = "root"
    password = "258258"
    scheme = "exam"
    port = "5432"
    protocol = "postgres"
    url = "localhost"

    engine = create_engine(
        f'{protocol}://{user_name}:{password}@{url}:{port}/{scheme}',
        pool_reset_on_return=False, pool_size=25, echo=False
    )
    db_session_maker = sessionmaker(autocommit=False, expire_on_commit=False, bind=engine)
    db_scoped_session = scoped_session(db_session_maker)

    @classmethod
    def get_session(cls):
        return cls.db_scoped_session()

    @classmethod
    def reflect_table(cls, table_name):
        from sqlalchemy import MetaData
        metadata = MetaData(bind=cls.engine, schema=cls.scheme)
        metadata.reflect(only=[table_name])
        table = metadata.tables[cls.scheme + '.' + table_name]
        return table

if __name__ == '__main__':
    print(DBManager.get_session().execute("SELECT 1"))
