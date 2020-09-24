from typing import List, Optional
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Query,
                     Security, status)
from magnet.database import get_db
from sqlalchemy.orm import Session
from . import actors, service, schemas
from .impl import enums

router = APIRouter()

@router.post("/zaif")
async def exec_zaif():
    exchange1 = actors.Exchange(name="zaif")
    exchange2 = actors.Exchange(name="bitflyer")

    profile = service.get_strategy_profile(user="test", profile_name="arbitrage")
    service.exec_zaif.delay(profile)
    return


@router.post("/bitflyer")
async def exec_bitflyer():
    exchange1 = actors.Exchange(name="zaif")
    exchange2 = actors.Exchange(name="bitflyer")

    profile = service.get_strategy_profile(user="test", profile_name="arbitrage")
    service.exec_bitflyer.delay(profile)
    return


@router.post("/etl")
async def get_all_chart():
    return await service.get_all_chart()
