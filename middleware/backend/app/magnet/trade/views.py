# from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Query,
#                      Security, status)
# from . import __actors, service, schemas

# router = APIRouter()
#
#
# @router.post("/zaif")
# async def exec_zaif():
#     exchange1 = __actors.Exchange(name="zaif")
#     exchange2 = __actors.Exchange(name="bitflyer")
#
#     profile = service.get_strategy_profile(user="test", profile_name="arbitrage")
#     service.exec_zaif.delay(profile)
#     return
#
#
# @router.post("/bitflyer")
# async def exec_bitflyer():
#     exchange1 = __actors.Exchange(name="zaif")
#     exchange2 = __actors.Exchange(name="bitflyer")
#
#     profile = service.get_strategy_profile(user="test", profile_name="arbitrage")
#     service.exec_bitflyer.delay(profile)
#     return
#
#
# router.post("/etl")(service.load_ohlc_by_laundering)


from typing import List
from magnet import get_db, Session, PagenationQuery, Depends, HTTPException, Env
from magnet.vendors import cbv, InferringRouter, TemplateView, build_exception, fastapi_funnel
from . import crud, schemas, etl

router = InferringRouter()
# brokers = Env.brokers


@cbv(router)
class Brokers:
    @router.get("/brokers")
    @fastapi_funnel
    async def index(self, q: PagenationQuery) -> List[str]:
        return crud.brokers.query().map(lambda x: x.__name__).skip(q.skip).take(q.limit).to_list()

    # @router.post("/")
    # async def create(self, data: schemas.Model.prefab(suffix="Create", exclude=("id",))) -> schemas.Model:
    #     return super().create(data=data)
    #
    # @router.get("/{id}")
    # async def get(self, id: int) -> schemas.Model:
    #     return super().get(id=id)
    #
    # @router.delete("/{id}/delete", status_code=200)
    # async def delete(self, id: int) -> int:
    #     return super().delete(id=id)
    #
    # @router.patch("/{id}/patch")
    # async def patch(self, id: int, data: schemas.Model.prefab(suffix="Patch", optionals=[...])) -> schemas.Model:
    #     return super().patch(id=id, data=data)
    #
    # @router.post("/{id}/copy")
    # async def copy(self, id: int) -> schemas.Model:
    #     return super().duplicate(id=id)


@cbv(router)
class Etl:
    db: Session = Depends(get_db)

    @router.get("/etl/load_all")
    async def load_all(self):
        all_result = {}
        result = await self.load_pairs()
        all_result["load_pairs"] = result

        result = await self.load_ohlc()
        all_result["load_ohlc"] = result

        return all_result

    @router.get("/etl/load_pairs")
    async def load_pairs(self):
        return await etl.load_pairs(self.db)

    @router.get("/etl/load_ohlc")
    async def load_ohlc(self):
        return await etl.load_ohlc(self.db)
