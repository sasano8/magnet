import locale
import json
from tzlocal import get_localzone
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.encoders import jsonable_encoder
from magnet import Env, logger
from typing import Iterable, Callable

system_locale = locale.getdefaultlocale()
language_code = system_locale[0]
encoding = system_locale[1]
local_tz = get_localzone()
if not language_code == "en_US":
    raise Exception(f"Not allowed language_code: {language_code}")

if not encoding == "UTF-8":
    raise Exception(f"Not allowed encoding: {encoding}")

if not str(local_tz) == "UTC":
    raise Exception(f"Not allowed timezone: {local_tz}")

SQLALCHEMY_DATABASE_URL = Env.databases["default"].get_connection_string()


def json_dumps(dic: dict):
    dic = jsonable_encoder(dic)
    s = json.dumps(dic, ensure_ascii=False)
    return s


def create_get_db(session_maker):
    def get_db() -> Iterable[Session]:
        # TODO: セッションはアプリケーションで一つのセッションを返すグローバルセッションと、
        db: Session = session_maker()
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
    return get_db


def create_production_engine():
    # TODO: トランザクション分離レベルの設定とテストをする。postgreSQLのデフォルトトランザクション分離レベルはread committedです。
    # read committedは、コミットされていないデータの最新情報やレコードを、異なるトランザクションから参照することができません。
    #  https://docs.sqlalchemy.org/en/13/dialects/postgresql.html?highlight=dialect#transaction-isolation-level
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"options": "-c timezone=utc"},
        json_serializer=json_dumps
    )
    session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    get_db_session = create_get_db(session_maker)
    return engine, get_db_session


def create_test_engine():
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        json_serializer=json_dumps
    )
    session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    get_db_session = create_get_db(session_maker)
    return engine, get_db_session


engine, get_db = create_production_engine()
get_db: Callable[[], Iterable[Session]] = get_db


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

