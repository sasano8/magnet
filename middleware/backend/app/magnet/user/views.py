from typing import List, Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (OAuth2PasswordRequestForm,
                              SecurityScopes)
from jwt import PyJWTError
from pydantic import ValidationError
from .utils import get_password_hash, verify_password, encode_access_token, decode_access_token, oauth2_schema
from magnet import get_db, TemplateView, PagenationQuery, Session, Linq
from magnet.vendors import cbv, InferringRouter, fastapi_funnel
from magnet.user import crud, models, schemas


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
        token_scopes = payload.get("scopes", [])
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, scopes=token_scopes)
    except (PyJWTError, ValidationError):
        raise credentials_exception

    user = crud.User(db).get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception

    # 要求に必要な権限を保持しているか
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


router = InferringRouter()





@cbv(router)
class GuestUserView(TemplateView[crud.User]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.User:
        return super().rep

    @router.post("/guest/login")
    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
        user = self.rep.get_user_by_username(form_data.username)
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

    @router.post("/guest")
    async def create(self, data: schemas.UserCreate) -> schemas.User:
        user = self.rep.get_user_by_username(data.email)
        if user:
            raise HTTPException(status_code=400, detail="Email already registerd")

        user_added_hash = schemas.UserCreate.construct(
            email=data.email,
            username=data.email,
            hashed_password=get_password_hash(data.password.get_secret_value())
        )
        return self.rep.create(user_added_hash)


@cbv(router)
class UserView(TemplateView[crud.User]):
    db: Session = Depends(get_db)
    current_user: models.User = Depends(get_current_user)

    @property
    def rep(self) -> crud.User:
        return super().rep

    @router.get("/")
    @fastapi_funnel
    async def index(self, q: PagenationQuery) -> List[schemas.User]:
        return super().index(skip=q.skip, limit=q.limit)

    # @router.get("/{id}")
    # async def get(self, id: int) -> schemas.User:
    #     return super().get(id=id)

    # /meがidだと認識されてしむため、パス設計をしなければ!!!!!
    @router.delete("/{id}/delete", status_code=200)
    async def delete(self, id: int) -> int:
        return super().delete(id=id)

    @router.patch("/{id}/patch")
    async def patch(self, id: int, data: schemas.User.prefab("Patch", optionals=[...])) -> schemas.User:
        return super().patch(id=id, data=data)


@cbv(router)
class UserMeView(TemplateView[crud.User]):
    db: Session = Depends(get_db)
    current_user: models.User = Security(get_current_active_user, scopes=["me"])

    @property
    def rep(self) -> crud.User:
        return super().rep

    @router.get("/me")
    async def get(self) -> schemas.User:
        return self.current_user

    @router.delete("/me/delete", status_code=200)
    async def delete(self) -> int:
        return super().delete(id=self.current_user.id)

    # @router.get("/me/items")
    # async def get_own_items(self, current_user: models.User = Security(get_current_active_user, scopes=["items"])):
    #     return [{"item_id": "Foo", "owner_ID": current_user.id}]




@cbv(router)
class UserItemView(TemplateView[crud.Item]):
    db: Session = Depends(get_db)
    current_user: models.User = Depends(get_current_user)

    @property
    def rep(self) -> crud.Item:
        return super().rep

    @router.get("/items")
    @fastapi_funnel
    async def index(self, q: PagenationQuery) -> List[schemas.Item]:
        return super().index(skip=q.skip, limit=q.limit)

