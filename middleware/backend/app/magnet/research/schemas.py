from typing import List, Optional
from pydantic import BaseModel
from magnet import config

class CaseNodeCreate(BaseModel):
    name: str


class CaseNodeBase(BaseModel):
    Config = config.ORM
    id: int
    name: str


class CaseNodeUpdate(BaseModel):
    Config = config.ORM
    id: Optional[int]
    name: Optional[str]


class TargetCreate(BaseModel):
    name: str
    node_id: int


class TargetBase(BaseModel):
    Config = config.ORM
    id: int
    name: str
    node_id: int


class TargetUpdate(BaseModel):
    Config = config.ORM
    id: Optional[int]
    name: Optional[str]
    node_id: Optional[int]
