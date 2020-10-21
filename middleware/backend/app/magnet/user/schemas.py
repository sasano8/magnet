from typing import List, Optional
from magnet import BaseModel
from pydantic import SecretStr

class ORM:
    orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class Item(BaseModel):
    Config = ORM

    id: int
    title: str
    description: str = None
    owner_id: int


class UserCreate(BaseModel):
    email: str
    password: SecretStr


class User(BaseModel):
    Config = ORM

    id: int
    email: str
    # password: str # セキュリティ観点上、値を返さない
    username: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    is_active: bool
    items: List[Item] = []
