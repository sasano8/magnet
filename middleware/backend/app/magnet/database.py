from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query, Session
from magnet import Env, logger
from typing import Iterable


SQLALCHEMY_DATABASE_URL = Env.databases["default"].get_connection_string()

if SQLALCHEMY_DATABASE_URL.startswith('sqlite'):
    logger.warning("sqliteはalembicのauto migrationに完全対応していません。")
    kwargs = {"check_same_thread": False}
else:
    kwargs = {}


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=kwargs
)
CreateSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Iterable[Session]:
    db: Session = CreateSession()
    try:
        yield db
        # db.commit()
    finally:
        # noinspection PyBroadException
        try:
            # In case of uncommit, it will be rolled back implicitly
            db.close()
        except Exception as e:
            logger.critical(exc_info=True)


# class Base:
#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__.lower()
#
#     # __table_args__ = {'mysql_engine': 'InnoDB'}
#
#     id = Column(Integer, primary_key=True)
#
#
# Base = declarative_base(cls=Base)
Base = declarative_base()

