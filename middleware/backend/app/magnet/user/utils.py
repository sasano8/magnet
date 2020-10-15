from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm,
                              SecurityScopes)
from passlib.context import CryptContext
from datetime import datetime, timedelta

import jwt
# from magnet import config
from magnet.env import Env

TOKEN_URL = Env.access_token.url
SECRET_KEY = Env.access_token.secret_key.get_secret_value()
ALGORITHM = Env.access_token.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = Env.access_token.expire_minutes

from libs.fastapi import security
authorizer = security.AccessToken(
    token_url=TOKEN_URL,
    secret_key=SECRET_KEY,
    algorithm=ALGORITHM,
    expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    scopes={"me": "Read information about the current user.", "items": "Read items."}
)

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=TOKEN_URL,
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def encode_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=expires_minutes)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
