from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Query,
                     Security, status)
from . import __actors, service, schemas

router = APIRouter()


@router.post("/zaif")
async def exec_zaif():
    exchange1 = __actors.Exchange(name="zaif")
    exchange2 = __actors.Exchange(name="bitflyer")

    profile = service.get_strategy_profile(user="test", profile_name="arbitrage")
    service.exec_zaif.delay(profile)
    return


@router.post("/bitflyer")
async def exec_bitflyer():
    exchange1 = __actors.Exchange(name="zaif")
    exchange2 = __actors.Exchange(name="bitflyer")

    profile = service.get_strategy_profile(user="test", profile_name="arbitrage")
    service.exec_bitflyer.delay(profile)
    return


router.post("/etl")(service.load_ohlc_by_laundering)
