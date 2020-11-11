from typing import List, Optional
from magnet import BaseModel


class Dummy(BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
