from sqlalchemy.orm import Session
from . import models
from libs.fastapi import GenericRepository


class User(GenericRepository[models.User]):
    pass


class Item(GenericRepository[models.Item]):
    pass


def get_user_by_name(db: Session, username: str):
    return User(db).query().filter(models.User.username == username).one()

