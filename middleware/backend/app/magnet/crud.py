from sqlalchemy.orm import Session

from . import models, schemas

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
    # from magnet.schemas import UserInDB
    # if username in db:
    #     user_dict = db[username]
    #     return UserInDB(**user_dict)



def get_user_by_email(db: Session, email: str):
    obj = db.query(models.User).filter(models.User.email == email).first()
    return obj

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate, hash_func = None):
    db_user = models.User(
        email=user.email,
        username=user.email,
        hashed_password=hash_func(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()


def get_items(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item