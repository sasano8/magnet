import asyncio

from . import crud, schemas
from .impl import enums
from .impl import exchanges as ex
from .impl import broker
from fastapi import HTTPException, Depends
from pydantic import create_model
# from workers import rabbitmq
from magnet import rabbitmq, Linq
from libs.generator import dump_pydantic_code_from_json
from pydantic import BaseModel
import json
import magnet.datastore.crud as datastore_crud
import magnet.datastore.schemas as datastore_schemas
from typing import List
import datetime


def get_exchange(name: enums.Exchange):
    obj = crud.exchanges.get(name)

    if not obj:
        raise HTTPException(status_code=404, detail=f"{name}: not found.")

    return obj


def get_strategy_profile(user:str, profile_name: str = "default"):
    return schemas.ProfilePrimitive(
        name="arbitrage",
        strategy="arbitrage",
        coin="BTC/JPY",
        markets=["zaif", "zaif"]
    )


def build_strategy_from_profile(profile: schemas.ProfilePrimitive):
    exchange1 = get_exchange(enums.Exchange.ZAIF)
    exchange2 = get_exchange(enums.Exchange.ZAIF)

    obj = schemas.Strategy(
        exchanges={exchange1, exchange2}
    )

    return obj

@rabbitmq.task
async def exec_zaif(profile: schemas.ProfilePrimitive):
    strategy = build_strategy_from_profile(profile)

    # シグナルを検知させたい

    # setはlistに変換しないとインデックスアクセスができない
    exchanges = list(strategy.exchanges)

    exchange1 = exchanges[0]
    # exchange2 = exchanges[1]

    exchange1 = ex.Zaif

    count = 0

    while count == 0:
        await asyncio.sleep(1)
        ticker = await broker.Zaif.get_ticker(enums.CurrencyPair.btc_jpy)
        print(ticker)


        coroutines = [
            exchange1.get_ticker(enums.CurrencyPair.btc_jpy),
            exchange1.get_currency_pairs(),
            # exchange1.get_info(),
            # exchange1.get_info2(),
            # exchange1.post_trade(
            #     currency_pair=exchange1.currency_pairs.xem_jpy.value,
            #     action="ask",
            #     price=1,
            #     amount=1
            # ),
            broker.Zaif.post_buy(
                currency_pair=exchange1.currency_pairs.xem_jpy,
                price=1,
                amount=1
            )
            # exchange1.post_create_position()
        ]

        tasks = map(lambda x: asyncio.create_task(x), coroutines)
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        for task in done:
            # 終了していない場合、結果が準備できるまでブロックする
            res = task.result()
            print("")
            print(dump_pydantic_code_from_json(__model_name="sample", data=res))
            print(" ")


        count += 1


@rabbitmq.task
async def exec_bitflyer(profile: schemas.ProfilePrimitive):
    strategy = build_strategy_from_profile(profile)

    exchange1 = ex.Bitflyer

    count = 0

    # result = await exchange1.get_markets()

    while count == 0:
        await asyncio.sleep(1)
        # ticker = await broker.Zaif.get_ticker(enums.CurrencyPair.btc_jpy)
        # print(ticker)


        coroutines = [
            # exchange1.get_markets(),
            # exchange1.get_board(product_code="ETH_BTC")
            exchange1.get_permissions(),
            # exchange1.post_sendchildorder(
            #     product_code="BTC_JPY",
            #     child_order_type="LIMIT",
            #     side="BUY",
            #     price=1159200,
            #     size=0.001,
            #     time_in_force="FOK"
            # )
            broker.Bitflyer.post_sell(currency_pair=None, price=1159200, amount=0.01)
        ]

        tasks = map(lambda x: asyncio.create_task(x), coroutines)
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        for task in done:
            # 終了していない場合、結果が準備できるまでブロックする
            res = task.result()

            print(res)

            # if not isinstance(res, BaseModel):
            #     print("")
            #     print(dump_pydantic_code_from_json(__model_name="sample", data=res))
            #     print("")
            #
            # else:
            #     print("")
            #     print(res)
            #     print("")


        count += 1


from magnet.database import get_db


async def load_ohlc_by_laundering(market: str = "bitfllyer", product: str = "bitcjpy", periods: int = 60 * 60 * 24, after: datetime.datetime = datetime.datetime(2010, 1, 1), db=Depends(get_db)):
    """指定したリソースの４本値を洗い替えする"""

    api = ex.CryptowatchAPI
    provider = "cryptowatch"

    def convert(obj) -> datastore_schemas.Ohlc:
        # import magnet.trade.impl.exchanges.cryptowat
        # obj: magnet.trade.impl.exchanges.cryptowat.Ohlc = obj

        return datastore_schemas.Ohlc(
            provider=provider,
            market=market,
            product=product,
            periods=periods,
            close_time=obj.close_time,
            open_price=obj.open_price,
            high_price=obj.high_price,
            low_price=obj.low_price,
            close_price=obj.close_price,
            volume=obj.volume,
            quote_volume=obj.quote_volume
        )

    result = await api.list_ohlc(market="bitflyer", product="btcjpy", periods=periods, after=after)
    mapped = map(convert, result)
    mapped = datastore_schemas.Ohlc.compute_technical(mapped)

    result = datastore_crud.CryptoOhlcDaily.bulk_insert_by_laundering(
        db=db,
        data=mapped,
        provider=provider,
        market=market,
        product=product,
        periods=periods,
        after=after
    )

    return result


