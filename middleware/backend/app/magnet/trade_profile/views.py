from typing import List
from magnet import get_db, Session, default_query, CommonQuery, Depends, HTTPException
from magnet.vendors import cbv, InferringRouter, TemplateView, build_exception
from . import crud, schemas, models

router = InferringRouter()


@cbv(router)
class TradeProfileView(TemplateView[crud.TradeProfile]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.TradeProfile:
        return super().rep

    @router.get("/template")
    async def index(self, q: CommonQuery = default_query) -> List[schemas.TradeProfile]:
        return super().index(skip=q.skip, limit=q.limit)

    @router.post("/template")
    async def create(self, data: schemas.TradeProfileCreate) -> schemas.TradeProfile:
        obj = self.rep.get_by_name(data.name)
        if obj:
            e = build_exception(
                status_code=422,
                loc=("name",),
                msg="すでに同名のテンプレートが存在します。",
            )
            raise e
        return super().create(data=data)

    @router.get("/template/{id}")
    async def get(self, id: int) -> schemas.TradeProfile:
        return super().get(id=id)

    @router.delete("/template/{id}/delete", status_code=200)
    async def delete(self, id: int) -> int:
        return super().delete(id=id)

    @router.patch("/template/{id}/patch")
    async def patch(self, id: int, data: schemas.TradeProfilePatch) -> schemas.TradeProfile:
        return super().patch(id=id, data=data)

    @router.post("/template/{id}/copy")
    async def copy(self, id: int) -> schemas.TradeProfile:
        return super().duplicate(id=id)

    @router.post("/template/{id}/copy_to_job")
    async def copy_to_job(self, id: int, job_name: str) -> schemas.TradeProfile:
        job_view = TradeJobView(db=self.db)
        obj = job_view.rep.get_by_name(job_name)
        if obj:
            e = build_exception(
                status_code=422,
                loc=("job_name",),
                msg="すでに同名のテンプレートが存在します。",
            )
            raise e
        obj = await self.get(id=id)
        obj = schemas.TradeProfileCreate.from_orm(obj)
        dic = dict(**obj.dict(exclude={"name"}), name=job_name)
        obj = schemas.TradeProfileCreate(**dic)
        created = await job_view.create(data=obj)
        return created


@cbv(router)
class TradeJobView(TemplateView[crud.TradeJob]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.TradeJob:
        return super().rep

    @router.get("/job")
    async def index(self, q: CommonQuery = default_query) -> List[schemas.TradeProfile]:
        return super().index(skip=q.skip, limit=q.limit)

    @router.post("/job")
    async def create(self, data: schemas.TradeProfileCreate) -> schemas.TradeProfile:
        obj = self.rep.get_by_name(data.name)
        if obj:
            e = build_exception(
                status_code=422,
                loc=("name",),
                msg="すでに同名のテンプレートが存在します。",
            )
            raise e
        return super().create(data=data)

    @router.get("/job/{id}")
    async def get(self, id: int) -> schemas.TradeProfile:
        return super().get(id=id)

    @router.delete("/job/{id}/delete", status_code=200)
    async def delete(self, id: int) -> int:
        return super().delete(id=id)

    @router.patch("/job/{id}/patch")
    async def patch(self, id: int, data: schemas.TradeProfilePatch) -> schemas.TradeProfile:
        return super().patch(id=id, data=data)

    @router.post("/job/{id}/copy")
    async def copy(self, id: int) -> schemas.TradeProfile:
        return super().duplicate(id=id)

    @router.post("/job/{id}/exec")
    async def exec(self, id: int) -> schemas.TradeProfile:
        p = await self.get(id=id)
        p = schemas.TradeProfile.from_orm(p)

        # name: str
        # description: str = ""
        p.provider
        p.market
        p.product
        p.periods
        # cron: str = ""
        # broker: str
        # order_id: float = None

        """
        過去データを読み込む
        分析する
        サインを検出する
        サインを分析し売買を行う
        注文を保持する
        """


        return p



