import json
from magnet import app, logger, depends_db, get_db, BaseModel
from . import schemas, crud

@app.on_event("startup")
async def initial_default_data():
    initial_data = [
        schemas.TradeProfile(
            id=1,
            name="bitcjpyゴールデンクロス・デッドクロス売買",
            description="単純移動平均線5 25から算出したクロスサイン時にドテン売買を行う。",
            provider="cryptwatch",
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
    ]

    logger.info(json.dumps((initial_data[0].dict()), indent=2, ensure_ascii=False))
    for db in get_db():
        crud.TradeProfile(db=db).upsert(data=initial_data[0])








# async def trade_btcjpy_cross_algorithm():
    # current_value = None
    # どういう処理にするか？
    # アルゴリズムが値を検証し、サインを出力する
    # サイン