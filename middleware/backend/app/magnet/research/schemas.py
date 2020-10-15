from typing import List, Optional
from magnet import config, BaseModel


class CaseNode(BaseModel):
    Config = config.ORM
    id: int
    name: str


class Target(BaseModel):
    Config = config.ORM
    id: int
    name: str
    node_id: int
