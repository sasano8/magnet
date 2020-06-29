from typing import List, Optional

from pydantic import BaseModel

class ORM:
    orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


# class ItemBase(BaseModel):
#     title: str
#     description: str = None

class ItemCreate(BaseModel):
    title: str
    description: str = None

class Item(BaseModel):
    Config = ORM

    id: int
    title: str
    description: str = None
    owner_id: int


# class UserBase(BaseModel):
#     pass

class UserCreate(BaseModel):
    email: str
    password : str

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

# class UserInDB(User):
#     hashed_password: str

