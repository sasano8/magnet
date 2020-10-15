from . import schemas, models
from sqlalchemy.orm import Session
import magnet.crawler.service as crawler


def instatiate_executor(input: schemas.DispatchCreate, db: Session = None):
    # webdriverを使う
    # postgreSQLに登録する
    # pipeline
    import magnet.ingester.service as ingester
    crawler_func = crawler.get_crawler_func_by_name(input.crawler_name)
    pipeline = ingester.get_ingester_by_name(input.pipeline_name)

    # TODO: conver_to_pydantic
    if not crawler_func:
        raise Exception("not found {}".format(input.crawler_name))

    if not pipeline:
        raise Exception("not found {}".format(input.pipeline_name))

    executor = pipeline(crawler=crawler_func, db=db)
    return executor
