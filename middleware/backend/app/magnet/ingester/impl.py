from pydantic import BaseModel
from typing import Any
from . import schemas, service
from magnet.log import logger


class PipelineBase(BaseModel):
    crawler: Any
    db: Any

    def __init__(self, **data: Any):
        super().__init__(**data)


class Postgress(PipelineBase):

    def __call__(self, input: schemas.CommonSchema):

        self.output(input)
        return

        for item in self.start_requests(input):
            item.detail = self.parse(item.detail)
            self.output(item)

        self.finalize()

    def start_requests(self, params: schemas.CommonSchema):
        yield from ()

    def parse(self, item: schemas.Detail):
        return item

    def output(self, input: schemas.CommonSchema):
        logger.info(input.detail)
        service.create(self.db, input)

    def finalize(self):
        pass




def dummy_func(self, payload):
    pass


pipeline = [
    dummy_func,
    dummy_func,
    dummy_func,
    dummy_func,
]

def exec_pipeline():

    db = {}
    driver = {}
    obj = {}
    data = {}

    for func in pipeline:
        current_obj = None
        for item in func(obj, obj):
            current_obj = func(obj, item)
