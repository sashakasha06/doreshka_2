from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

SqlAlchemyBase = declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    engine = create_engine(conn_str, echo=True)  # echo=True для отладки
    __factory = sessionmaker(bind=engine)

    # Импорт моделей для создания таблиц
    from . import users, jobs
    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    global __factory
    if not __factory:
        raise RuntimeError("Сначала вызовите global_init()!")
    return __factory()