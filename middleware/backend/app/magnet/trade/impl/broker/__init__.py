from .. import exchanges
from libs.decorators import Instantiate

@Instantiate
class Zaif:
    async def get_ticker(self, currency_pair: exchanges.Zaif.currency_pairs):
        return await exchanges.Zaif.get_ticker(currency_pair=currency_pair)

    async def post_buy(self, currency_pair: exchanges.Zaif.currency_pairs, price, amount: float, limit: float = None, comment: str = None):
        return await exchanges.Zaif.post_trade(
            currency_pair=currency_pair.value,
            action="bid",
            price=1,
            amount=1,
            limit=limit,
            comment=comment
        )

    async def post_sell(self, currency_pair: exchanges.Zaif.currency_pairs, price, amount: float, limit: float = None, comment: str = None):
        return await exchanges.Zaif.post_trade(
            currency_pair=currency_pair.value,
            action="ask",
            price=1,
            amount=1,
            limit=limit,
            comment=comment
        )


@Instantiate
class Bitflyer:
    async def get_ticker(self, currency_pair: exchanges.Zaif.currency_pairs):
        return await exchanges.Zaif.get_ticker(currency_pair=currency_pair)

    async def post_buy(self, currency_pair: exchanges.Zaif.currency_pairs, price, amount: float, limit: float = None, comment: str = None):
        return await exchanges.Bitflyer.post_sendchildorder(
                product_code="FX_BTC_JPY",
                child_order_type="LIMIT",
                side="BUY",
                price=1159200,
                size=0.001,
                time_in_force="FOK"
            )

    async def post_sell(self, currency_pair: exchanges.Zaif.currency_pairs, price: float, amount: float, limit: float = None, comment: str = None):
        # return await exchanges.Bitflyer.post_sendchildorder(
        #     product_code="BTC_JPY",
        #     child_order_type="LIMIT",
        #     side="SELL",
        #     price=price,
        #     size=amount,
        #     time_in_force="FOK"
        # )

        return await exchanges.Bitflyer.post_sendchildorder(
                product_code="FX_BTC_JPY",
                child_order_type="LIMIT",
                side="SELL",
                price=price,
                size=amount,
                time_in_force="FOK"
            )