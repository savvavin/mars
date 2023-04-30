import sqlalchemy as sqla
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_name):
    global __factory

    if __factory:
        return

    conn_str = f"sqlite:///{db_name}?check_same_thread=false"
    engine = sqla.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
