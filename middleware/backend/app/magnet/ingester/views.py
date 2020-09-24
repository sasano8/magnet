from typing import List, Optional
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Query,
                     Security, status)
from magnet.database import get_db
from sqlalchemy.orm import Session
from . import schemas, service

router = APIRouter()


@router.post("/job")
async def create_job(input: schemas.JobCreate, db: Session = Depends(get_db)):
    obj = service.create_job(db, input)
    return obj

@router.get("/queue", response_model=List[schemas.CommonSchema])
async def list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.list(db, skip=skip, limit=limit)


@router.get("/queue/{id}", response_model=schemas.CommonSchema)
async def get(id: int, db: Session = Depends(get_db)):
    obj = service.get(db, id)
    return obj


@router.post("/queue", response_model=schemas.CommonSchema)
async def create(input: schemas.CommonSchema, db: Session = Depends(get_db)):
    return service.create(db, input)


async def update(db: Session = Depends(get_db)):
    raise NotImplementedError()


async def digest(id: int, db: Session = Depends(get_db)):
    return service.digest(db, id=id, delete_on_complete=True)


@router.delete("/queue/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    return service.delete(db, id=id)


@router.delete("/queue/delete_all/")
async def delete_all(db: Session = Depends(get_db)):
    return service.delete_all(db)