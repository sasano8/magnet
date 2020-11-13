from magnet import BaseModel

# traderの責務
# 独自サインを検出する
# 意思決定を行う

# brokerの責務
# 発注する


class MarketBase(BaseModel):
    db = None
    trader = None
    broker = None
    scheduler = None
    logger = None

    def init(self):
        trader.broker = broker

    def run(self):
        ticker = broker.get_ticker()
        trader.notify(ticker)
