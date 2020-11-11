import json
from libs.linq import Linq
from magnet import app, logger, depends_db, get_db, BaseModel
from . import schemas, crud, views

# イベントは並列でなく直列に実行される
# @app.on_event("startup")
# async def loop1():
#     import asyncio
#     for item in range(3):
#         print("aaaaaaaaaaaaaaaaaaaaaaa")
#         await asyncio.sleep(10)
#
#
# @app.on_event("startup")
# async def loop2():
#     import asyncio
#     for item in range(3):
#         print("bbbbbbbbbb")
#         await asyncio.sleep(10)
#


@views.router.on_event("startup")
async def upsert_default_data():
    default_profiles = Linq([
        schemas.TradeProfile(
            id=1,
            name="bitcjpyゴールデンクロス・デッドクロス売買",
            description="単純移動平均線5 25から算出したクロスサイン時にドテン売買を行う。",
            provider="cryptowatch",
            market="bitflyer",
            product="btcjpy",
            periods=60 * 60 * 24,
            cron="",
            broker="bitflyer",
            trade_rule=schemas.RuleTrade(
                entry=schemas.RulePosition(
                    name="資産の20%を投資",
                    algorithm="default",
                    amount=schemas.RuleAmount(target="wallet", mode="rate", value=0.2)
                ),
                profit=schemas.RulePosition(
                    name="注文を全て利確",
                    amount=schemas.RuleAmount(target="order", mode="all")
                ),
                losscut=schemas.RulePosition(name="ロスカットなし")
            )
        )
    ])

    for db in get_db():
        rep = crud.TradeProfile(db=db)
        default_profiles.dispatch(rep.upsert)
