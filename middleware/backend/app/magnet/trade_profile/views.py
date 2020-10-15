from typing import List
from magnet import get_db, Session, default_query, CommonQuery, Depends
from magnet.vendors import cbv, InferringRouter, TemplateView
from . import crud, schemas

router = InferringRouter()


@cbv(router)
class TradeProfileView(TemplateView[crud.TradeProfile]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.TradeProfile:
        return super().rep

    @router.get("/")
    async def index(self, q: CommonQuery = default_query) -> List[schemas.TradeProfile]:
        return super().index(skip=q.skip, limit=q.limit)

    @router.post("/")
    async def create(self, data: schemas.TradeProfile.transform("Create", exclude=["id"])) -> schemas.TradeProfile:
        return super().create(data=data)

    @router.get("/{id}")
    async def get(self, id: int) -> schemas.TradeProfile:
        return super().get(id=id)

    @router.delete("/{id}/delete", status_code=200)
    async def delete(self, id: int) -> int:
        return super().delete(id=id)

    @router.patch("/{id}/patch")
    async def patch(self, id: int, data: schemas.TradeProfile.transform("Patch", optionals=[...])) -> schemas.TradeProfile:
        return super().patch(id=id, data=data)

    @router.post("/{id}/copy")
    async def copy(self, id: int) -> schemas.TradeProfile:
        return super().duplicate(id=id)
