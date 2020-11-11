from typing import List, Optional
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Query,
                     Security, status)
from magnet.database import get_db
from sqlalchemy.orm import Session
from . import schemas, crud, impl
from magnet import PagenationQuery
from magnet.vendors import cbv, InferringRouter, TemplateView, fastapi_funnel
from magnet.executor import worker

JOBGROUP_ROOT_ID = 0
router = APIRouter()


router = InferringRouter()


def get_ingester_by_name(ingester_name: str):
    if "postgres" == ingester_name:
        return impl.Postgress
    elif "elastic" == ingester_name:
        raise NotImplementedError()
    else:
        raise KeyError()


@cbv(router)
class IngesterJobGroupView(TemplateView[crud.IngesterJobGroup]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.IngesterJobGroup:
        return super().rep

    def get_or_create_jobgroup_root(self):
        rep = self.rep
        job_group = rep.get(id=JOBGROUP_ROOT_ID)

        if job_group is None:
            obj = schemas.JobGroupCreate(
                id=JOBGROUP_ROOT_ID,
                description="root",
                is_system=True
            )
            job_group = rep.create(obj)

        return job_group


@cbv(router)
class IngesterJobView(TemplateView[crud.IngesterJob]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.IngesterJob:
        return super().rep

    @router.post("/job")
    async def create(self, data: schemas.JobCreate) -> schemas.JobCreate:
        db = self.db
        r_job = self.rep
        r_job_group = IngesterJobGroupView(db=db)

        if data.jobgroup_id is None:
            data.jobgroup_id = JOBGROUP_ROOT_ID

        if data.jobgroup_id == JOBGROUP_ROOT_ID:
            jobgroup = r_job_group.get_or_create_jobgroup_root()
        else:
            jobgroup = r_job_group.get(id=data.jobgroup_id)
            if jobgroup is None:
                raise HTTPException(status_code=404, detail="Not found a job group.")

        dic = data.dict(exclude={"jobgroup_id"})
        job = r_job.model(**dic)

        job.parent_id = jobgroup.id
        db.add(job)
        db.commit()
        db.refresh(job)
        self.exec_job_by_id(job.id)
        return job

    async def exec_job_by_id(self, id: int):
        """
        キューにジョブを送出する。
        """
        rep = self.rep
        job = rep.get(id=id)
        if not job:
            raise HTTPException(status_code=404, detail="not found id.")

        payload = schemas.CommonSchema.from_orm(job)
        payload = schemas.TaskCreate(**payload.dict())

        try:
            worker.exec_job.delay(job=payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@cbv(router)
class IngesterView(TemplateView[crud.Ingester]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.Ingester:
        return super().rep

    @router.get("/queue")
    @fastapi_funnel
    async def index(self, q: PagenationQuery) -> List[schemas.CommonSchema]:
        return super().index(skip=q.skip, limit=q.limit)

    @router.post("/queue")
    async def create(self, data: schemas.CommonSchema) -> schemas.CommonSchema:
        return super().create(data=data)

    @router.get("/queue/{id}")
    async def get(self, id: int) -> schemas.CommonSchema:
        return super().get(id=id)

    @router.delete("/queue/{id}/delete", status_code=200)
    async def delete(self, id: int) -> int:
        return super().delete(id=id)

    # @router.patch("/queue{id}/patch")
    # async def patch(self, id: int, data: schemas.TradeProfile.transform("Patch", optionals=[...])) -> schemas.TradeProfile:
    #     return super().patch(id=id, data=data)
    #
    # @router.post("/queue{id}/copy")
    # async def copy(self, id: int) -> schemas.TradeProfile:
    #     return super().duplicate(id=id)

    @router.delete("/queue/delete_all", status_code=200)
    async def delete_all(self) -> int:
        return super().delete_all()

    @router.post("/queue/{id}/digest", status_code=200)
    async def digest(self, id: int) -> int:
        """指定したキューを消化する"""
        # return service.digest(db, id=id, delete_on_complete=True)
        raise NotImplementedError()

