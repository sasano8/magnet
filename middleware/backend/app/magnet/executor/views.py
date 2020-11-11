from typing import List, Optional
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from . import schemas, worker, crud
from magnet.ingester import schemas as ingester
from magnet import get_db, PagenationQuery, TemplateView, Depends
from magnet.vendors import cbv, InferringRouter, fastapi_funnel


router = InferringRouter()


@cbv(router)
class ExecutorView(TemplateView[crud.Executor]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.Executor:
        return super().rep

    @router.get("/")
    @fastapi_funnel
    async def index(self, q: PagenationQuery) -> List[schemas.ExecutorBase]:
        return super().index(skip=q.skip, limit=q.limit)

    @router.post("/")
    async def create(self, data: schemas.ExecutorCreate, is_system: bool = False) -> schemas.ExecutorBase:
        dic = data.dict()
        dic["is_system"] = is_system
        # dic = {"is_system": is_system, **data.dict()} こうできるかも
        obj = schemas.ExecutorBase(**dic)
        return super().create(data=data)

    @router.post("/execute", status_code=status.HTTP_202_ACCEPTED)
    async def request_job(self, data: ingester.TaskCreate):
        try:
            worker.exec_job.delay(data)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

