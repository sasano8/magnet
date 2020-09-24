from . import schemas, models
from sqlalchemy.orm import Session
import magnet.crawler.service as crawler
import magnet.ingester.service as ingester
from . import crud


def list_executor(db: Session, skip, limit):
    return crud.Executor.list(db, skip=skip, limit=limit)


def create_executor(db: Session, input: schemas.ExecutorCreate, is_system: bool = False):
    # TODO: もっとかっこいいマージ方法は？
    dic = input.dict()
    dic["is_system"] = is_system
    obj = schemas.ExecutorBase(**dic)
    return crud.Executor.create(db, obj)


def instatiate_executor(input: schemas.DispatchCreate, db: Session = None):
    # webdriverを使う
    # postgreSQLに登録する
    # pipeline
    crawler_func = crawler.get_crawler_func_by_name(input.crawler_name)
    pipeline = ingester.get_ingester_by_name(input.pipeline_name)

    # TODO: conver_to_pydantic
    if not crawler_func:
        raise Exception("not found {}".format(input.crawler_name))

    if not pipeline:
        raise Exception("not found {}".format(input.pipeline_name))

    executor = pipeline(crawler=crawler_func, db=db)
    return executor
