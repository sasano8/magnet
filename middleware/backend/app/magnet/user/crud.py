from sqlalchemy.orm import Session
from libs.decorators import Instantiate
from . import models, schemas
from magnet.database import GenericRepository

# rep_user = Repository(
#     sqlalchemy_model=models.User
# )

# rep_item = Repository(
#     sqlalchemy_model=models.Item
# )


@Instantiate
class User(GenericRepository[models.User]):
    pass


@Instantiate
class Item(GenericRepository[models.Item]):
    pass


def query_user(db: Session):
    return User.list(db)
    # return db.query(models.User)


def query_item(db: Session):
    return db.query(models.Item)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return User.list(db, skip=skip, limit=limit)


# def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
#     db_user = models.User(
#         email=user.email, username=user.email, hashed_password=hashed_password
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def delete_user(db: Session, user_id: int):
    query_user(db).filter(models.User.id == user_id).delete()
    db.commit()


def get_user(db: Session, user_id: int) -> models.User:
    return query_user(db).filter(models.User.id == user_id).one()

def update_user(db: Session, user: schemas.User):
    db_user = get_user(db, user_id=user.id)
    update_data = user.dict()
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_name(db: Session, username: str):
    return query_user(db).filter(models.User.username == username).one()



# def get_user_by_email(db: Session, email: str):
#     obj = query_user(db).filter(models.User.email == email).first()
#     return obj


def get_items(db: Session, skip: int = 0, limit: int = 0):
    return query_item(db).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
