import hashlib
import random

class Watcher():
    pass


class Wallet():
    pass


class Evalutor():
    pass


class Exchange():
    def __init__(self, name):
        self.name = name
        self.current_value = 10

    def get_price(self, coin_type):
        ticker = random.uniform(-0.2, 0.4)
        self.current_value += ticker
        return self.current_value

    def buy(self, coin_type: str):
        print("[BUY]{}:{}".format(self.name, self.current_value))

    def sell(self, coin_type: str):
        print("[SELL]{}:{}".format(self.name, self.current_value))


def evalute_arbitrage(price1, price2):
    avarage = (price1 + price2) / 2
    diff = max(price1, price2) - avarage
    ratio = diff / avarage
    return ratio


# ２つの取引所間で16円 17円 だった場合、そのレシオは0.03となる。

import asyncio

POSITION_RATIO = 0.015
RESOLUTION_RATIO = POSITION_RATIO / 1.8








# def sign_params(secret_key, nonce: int, method: str, type: str = "margin"):




async def start_arbitrage_tmp(exchange1, exchange2):

    count = 100
    current_count = 0
    position = False

    while current_count < count :
        # TODO: signal監視
        COIN_TYPE = "BTC/JPY"
        func_buy = None
        func_sell = None

        while position == False and current_count < count:
            await asyncio.sleep(1)

            price1 = exchange1.get_price(COIN_TYPE)
            price2 = exchange2.get_price(COIN_TYPE)

            ratio = evalute_arbitrage(price1, price2)
            print("ratio: {}".format(ratio))

            if ratio >= POSITION_RATIO:
                if price1 > price2:
                    exchange1.sell(COIN_TYPE)
                    exchange2.buy(COIN_TYPE)

                    func_buy = lambda: exchange1.buy(COIN_TYPE)
                    func_sell = lambda: exchange2.sell(COIN_TYPE)

                else:
                    exchange2.sell(COIN_TYPE)
                    exchange1.buy(COIN_TYPE)

                    func_buy = lambda: exchange2.buy(COIN_TYPE)
                    func_sell = lambda: exchange1.sell(COIN_TYPE)

                position = True

            current_count += 1


        while position == True and current_count < count:
            await asyncio.sleep(1)

            price1 = exchange1.get_price(COIN_TYPE)
            price2 = exchange2.get_price(COIN_TYPE)

            ratio = evalute_arbitrage(price1, price2)
            print("ratio: {}".format(ratio))

            if RESOLUTION_RATIO >= ratio:
                func_buy()
                func_sell()
                position = False

            current_count += 1

