import datetime
from magnet.trade.service import load_ohlc_by_laundering
from magnet.database import get_db
from magnet.datastore import crud


async def trade_btcjpy():
    db = get_db().__iter__().__next__()
    provider = "cryptwatch"
    market = "bitflyer"
    product = "btcjpy"
    periods = 60 * 60 * 24
    after = datetime.datetime(2010, 1, 1)

    # 1. cryptwatchからデータ取り込み
    # 2. サイン検出
    result = await load_ohlc_by_laundering(
        market=market,
        product=product,
        periods=periods,
        after=after,
        db=db
    )

    # 3. データ再ロード
    crud.CryptoOhlcDaily.filter_partition(
        db,
        provider=provider,
        market=market,
        product=product,
        periods=periods,
        after=after,
        skip=0,
        limit=10000000,
    )
    # 4. アルゴリズムプロファイルロード
    # 5. アルゴリズムロード
    # 6. 残高取得

    broker = {}


    # オーダー決定
    # 仮想注文登録
    # 注文

