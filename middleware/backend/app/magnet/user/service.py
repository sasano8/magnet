from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, models, utils


def list_user(db: Session, skip: int = 0, limit: int = 100):
    return crud.User.list(db, skip=skip, limit=limit)


def create_user(db: Session, user: schemas.UserCreate):
    db_user = crud.User.query(db).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registerd")

    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(
        email=user.email, username=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    obj = crud.User.query(db).filter(models.User.email == email).first()
    return obj


def delete_user(db: Session, id: int):
    return crud.User.delete(db, id=id)

