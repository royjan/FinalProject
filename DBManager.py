from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBManager:
    user_name = "root"
    password = "258258"
    scheme = "exam"
    port = "3306"
    protocol = "mysql+pymysql"
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
