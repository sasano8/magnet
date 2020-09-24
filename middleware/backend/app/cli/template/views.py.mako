from typing import List, Optional
from fastapi import (APIRouter, Depends, HTTPException, Query, Security, status)
from sqlalchemy.orm import Session

router = APIRouter()

# DEPEND_DB = db: Session = Depends(get_db)


@router.get("/")
async def list(skip: int = 0, limit: int = 100, ${DEPEND_DB}):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{id}")
async def get_by_id(id: int, ${DEPEND_DB}):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/")
async def create(schema, ${DEPEND_DB}):
    pass


@router.delete("/{id}")
async def delete_by_id(id: int, ${DEPEND_DB}):
    pass


@router.put("/")
async def update_by_id(schema, ${DEPEND_DB}):
    pass
