from pydantic import BaseModel
from typing import List, Any


class Exception(BaseModel):
    pass


class BulkResult(BaseModel):
    deleted: int
    inserted: int
    errors: List[Any]


class Page(BaseModel):
    pass