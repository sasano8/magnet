import logging
from typing import List, Optional

from fastapi import (APIRouter, Depends, HTTPException, Query,
                     Security, status)
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm,
                              SecurityScopes)
from jwt import PyJWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from magnet.database import SessionLocal, engine
from magnet.user import crud, models, schemas, service
from .utils import get_password_hash, verify_password, encode_access_token, decode_access_token, oauth2_schema
from magnet.database import get_db

router = APIRouter()

# TODO: config.loggerにする
logger = logging.getLogger("magnet")
logger.setLevel("DEBUG")


@router.post("/token", response_model=schemas.Token)
async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_name(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = encode_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_minutes=30,
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(username=username, scopes=token_scopes)
    except (PyJWTError, ValidationError):
        raise credentials_exception

    user = crud.get_user_by_name(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions.",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


async def get_current_active_user(
    current_user: models.User = Security(get_current_user, scopes=["me"])
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(
    current_user: models.User = Security(
        get_current_active_user, scopes=["items"]
    )
):
    return [{"item_id": "Foo", "owner_ID": current_user.id}]



@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # users = crud.get_users(db, skip=skip, limit=limit)
    users = service.list_user(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # db_user = crud.get_user_by_email(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registerd")
    #
    # # created = crud.create_user(db=db, user=user, hashed_password=get_password_hash(user.password))
    # # hashed_password = get_password_hash(user.password)
    created = service.create_user(db, user=user)
    return created


@router.delete("/", status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User id not found.")
    crud.delete_user(db, user_id=user_id)



@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
    return crud.update_user(db, user)



@router.post("/{user_id}", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items



@router.get("/status/")
async def read_system_status(current_user: models.User = Depends(get_current_user)):
    return {"status": "ok"}
