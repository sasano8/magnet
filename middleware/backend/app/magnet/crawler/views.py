from typing import List, Optional
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Query,
                     Security, status)
from magnet.database import get_db
from sqlalchemy.orm import Session
from . import service, crud
from libs import decorators

router = APIRouter()


@router.get("/", response_model=List[str])
async def list_crawler():
    mapping = map(lambda key_value: key_value[0], crud.crawlers.list())
    arr = list(mapping)
    return arr
