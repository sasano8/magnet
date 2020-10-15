from typing import List, Optional
from fastapi import (APIRouter, Depends, HTTPException, Query,
                     Security, status)
from fastapi.security import (OAuth2PasswordRequestForm,
                              SecurityScopes)
from jwt import PyJWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from magnet.user import crud, models, schemas
from .utils import get_password_hash, verify_password, encode_access_token, decode_access_token, oauth2_schema
from magnet import get_db, TemplateView, CommonQuery, default_query
from magnet.vendors import cbv, InferringRouter

router = APIRouter()


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


cbvrouter = InferringRouter()


@cbv(cbvrouter)
class UserView(TemplateView[crud.User]):
    db: Session = Depends(get_db)
    current_user: models.User = Depends(get_current_user)

    @property
    def rep(self) -> crud.User:
        return super().rep

    @cbvrouter.get("/")
    async def index(self, q: CommonQuery = default_query) -> List[schemas.User]:
        return super().index(skip=q.skip, limit=q.limit)

    @cbvrouter.post("/")
    async def create(self, data: schemas.UserCreate) -> schemas.User:
        user = self.rep.query().filter(models.User.email == data.email).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registerd")

        hashed_password = get_password_hash(data.password)
        user = models.User(
            email=user.email, username=user.email, hashed_password=hashed_password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    @cbvrouter.get("/{id}")
    async def get(self, id: int) -> schemas.User:
        return super().get(id=id)

    @cbvrouter.delete("/{id}/delete", status_code=200)
    async def delete(self, id: int) -> int:
        return super().delete(id=id)

    @cbvrouter.patch("/{id}/patch")
    async def patch(self, id: int, data: schemas.User.transform("Patch", optionals=[...])) -> schemas.User:
        return super().patch(id=id, data=data)

    # @router.post("/{id}/copy")
    # def copy(self, id: int) -> schemas.TradeProfile:
    #     return super().duplicate(id=id)


@cbv(cbvrouter)
class UserMeView(TemplateView[crud.User]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.User:
        return super().rep

    @cbvrouter.get("/me")
    async def get(self, id: int, current_user: models.User = Depends(get_current_user)) -> schemas.User:
        return current_user

    @cbvrouter.get("/me/items")
    async def get_own_items(self, id: int,
            current_user: models.User = Security(get_current_active_user, scopes=["items"])):
        return [{"item_id": "Foo", "owner_ID": current_user.id}]


@cbv(cbvrouter)
class UserItemView(TemplateView[crud.Item]):
    db: Session = Depends(get_db)
    current_user: models.User = Depends(get_current_user)

    @property
    def rep(self) -> crud.Item:
        return super().rep

    @cbvrouter.get("/items")
    async def index(self, q: CommonQuery = default_query) -> List[schemas.Item]:
        return super().index(skip=q.skip, limit=q.limit)

    # @cbvrouter.post("/")
    # async def create(self, data: schemas.TradeProfile.transform("Create", exclude=["id"])) -> schemas.TradeProfile:
    #     return super().create(data=data)
    #
    # @cbvrouter.get("/{id}")
    # async def get(self, id: int) -> schemas.TradeProfile:
    #     return super().get(id=id)
    #
    # @cbvrouter.delete("/{id}/delete", status_code=200)
    # async def delete(self, id: int) -> int:
    #     return super().delete(id=id)
    #
    # @cbvrouter.patch("/{id}/patch")
    # async def patch(self, id: int, data: schemas.TradeProfile.transform("Patch", optionals=[...])) -> schemas.TradeProfile:
    #     return super().patch(id=id, data=data)
    #
    # @router.post("/{id}/copy")
    # async def copy(self, id: int) -> schemas.TradeProfile:
    #     return super().duplicate(id=id)
