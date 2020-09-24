from typing import List, Optional
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Query,
                     Security, status)
from sqlalchemy.orm import Session
from . import schemas, service, worker
from magnet.database import get_db
from magnet.ingester import schemas as ingester

router = APIRouter()


@router.get("/", response_model=List[schemas.ExecutorBase])
async def list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.list_executor(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.ExecutorBase)
async def create(input: schemas.ExecutorCreate, db: Session = Depends(get_db)):
    return service.create_executor(db, input, is_system=False)


@router.post("/job/", status_code=status.HTTP_202_ACCEPTED)
async def request_job(task: ingester.TaskCreate):
    try:
        worker.exec_job.delay(task)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
