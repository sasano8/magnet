from typing import List
from magnet import get_db, Session, PagenationQuery, Depends, HTTPException, Env
from magnet.vendors import cbv, InferringRouter, TemplateView, build_exception, fastapi_funnel
from . import crud, schemas

router = InferringRouter()


@cbv(router)
class Dummy(TemplateView[crud.Dummy]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.Dummy:
        return super().rep

    @router.get("/")
    @fastapi_funnel
    async def index(self, q: PagenationQuery) -> List[schemas.Dummy]:
        return super().index(skip=q.skip, limit=q.limit)

    @router.post("/")
    async def create(self, data: schemas.Dummy.prefab(suffix="Create", exclude=("id",))) -> schemas.Dummy:
        return super().create(data=data)

    @router.get("/{id}")
    async def get(self, id: int) -> schemas.Dummy:
        return super().get(id=id)

    @router.delete("/{id}/delete", status_code=200)
    async def delete(self, id: int) -> int:
        return super().delete(id=id)

    @router.patch("/{id}/patch")
    async def patch(self, id: int, data: schemas.Dummy.prefab(suffix="Patch", optionals=[...])) -> schemas.Dummy:
        return super().patch(id=id, data=data)

    @router.post("/{id}/copy")
    async def copy(self, id: int) -> schemas.Dummy:
        return super().duplicate(id=id)
