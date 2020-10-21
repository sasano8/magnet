# from sqlalchemy.orm import Session
from . import models
from libs.fastapi import GenericRepository


class User(GenericRepository[models.User]):
    def get_user_by_username(self, username: str):
        return self.query().filter(models.User.username == username).one_or_none()


class Item(GenericRepository[models.Item]):
    pass


# def get_user_by_name(db: Session, username: str):
#     return User(db).query().filter(models.User.username == username).one()

