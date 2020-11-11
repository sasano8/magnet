import datetime
from magnet.database import get_db
from magnet.datastore import crud, schemas
from .impl import exchanges


async def load_pairs(db, /):
    api = exchanges.CryptowatchAPI
    provider = "cryptowatch"
    data = await api.get_pairs()
    mapped = [schemas.Pairs(provider="cryptowatch", symbol=x.symbol).dict() for x in data]

    rep = crud.CryptoPairs(db)
    result = rep.bulk_insert_by_laundering(
        data=mapped,
        provider=provider
    )

    return result


async def load_ohlc(db, /, market: str = "bitflyer", product: str = "btcjpy", periods: int = 60 * 60 * 24, after: datetime.datetime = datetime.datetime(2010, 1, 1)):
    """指定したリソースの４本値を洗い替えする"""

    api = exchanges.CryptowatchAPI
    provider = "cryptowatch"

    def convert(obj) -> schemas.Ohlc:
        # import magnet.trade.impl.exchanges.cryptowat
        # obj: magnet.trade.impl.exchanges.cryptowat.Ohlc = obj

        return schemas.Ohlc(
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
    mapped = schemas.Ohlc.compute_technical(mapped)

    rep = crud.CryptoOhlcDaily(db)
    result = rep.bulk_insert_by_laundering(
        rows=mapped,
        provider=provider,
        market=market,
        product=product,
        periods=periods,
        after=after
    )

    return result