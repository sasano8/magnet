from typing import Literal
from . import models, schemas
from libs.decorators import Instantiate
from libs.fastapi import GenericRepository
from sqlalchemy.orm import Session, Query
import datetime
from typing import Iterable, Tuple, List, Union
from libs.linq import Linq
from magnet import schemas as common_schema


class CryptoPairs(GenericRepository[models.CryptoPairs]):
    def filter(self, provider: str) -> Query:
        m = models.CryptoPairs
        return self.query().filter(
            m.provider == provider,
        )

    def bulk_insert_by_laundering(self, data: Iterable[schemas.Pairs], provider: str = "cryptowatch") -> common_schema.BulkResult:
        """
        指定した条件のデータを削除した後、指定したデータを登録する。（洗い替え方式）
        戻り値に削除件数と登録件数を返す。
        """
        errors = []
        delete_query = self.filter(
            provider=provider,
        )

        deleted, inserted = self.bulk_delete_insert(
            delete_query=delete_query,
            rows=data,
            auto_commit=False
        )

        if len(errors):
            self.db.rollback()
            raise Exception(str(errors))
        else:
            self.db.commit()

        return common_schema.BulkResult(
            deleted=deleted,
            inserted=inserted,
            errors=errors
        )


class CryptoOhlcDaily(GenericRepository[models.CryptoOhlc]):
    def _filter(self, provider: str, market: str, product: str, periods: int, after: datetime.datetime) -> Query:
        m = models.CryptoOhlc

        return self.query().filter(
            m.provider == provider,
            m.product == product,
            m.market == market,
            m.periods == periods,
            m.close_time >= after
        )

    def filter_partition(self, provider: str = "cryptowatch", market: str = "bitfllyer", product: str = "btcjpy", periods: int = 60 * 60 * 24, after: datetime.datetime = datetime.datetime(2010, 1, 1)) -> Union[Iterable[models.CryptoOhlc], Query]:
        query = self._filter(
            provider=provider,
            product=product,
            market=market,
            periods=periods,
            after=after
        )

        return query

    def select_close_date(self, provider, market, product, periods, after: datetime.datetime = datetime.datetime(2010, 1, 1), until: datetime.date = None, order_by: Literal["asc", "desc"] = "asc"):
        if order_by == "asc":
            sort = self.model.close_time.asc()
        elif order_by == "desc":
            sort = self.model.close_time.desc()
        else:
            raise Exception()
        m = self.model
        query = self.select(m.close_time).filter(
            m.provider == provider,
            m.market == market,
            m.product == product,
            m.periods == periods,
            m.close_time >= after,
            m.close_time <= until,
        ).order_by(sort)
        return query

    def get_ticker(self, provider, market, product, periods, close_time: datetime.date):
        m = self.model

        result = self.filter(
            m.provider == provider,
            m.market == market,
            m.product == product,
            m.periods == periods,
            m.close_time == close_time
        ).one_or_none()
        return result

    def bulk_insert_by_laundering(self, rows: Iterable[schemas.Ohlc], provider: str = "cryptowatch", market: str = "bitfllyer", product: str = "btcjpy", periods: int = 60 * 60 * 24, after: datetime.datetime = datetime.datetime(2010, 1, 1)) -> common_schema.BulkResult:
        """
        指定した条件のデータを削除した後、指定したデータを登録する。（洗い替え方式）
        戻り値に削除件数と登録件数を返す。
        """
        errors = []
        rows = Linq(rows).hook_if(lambda index, x: not all([
            x.provider == provider,
            x.market == market,
            x.product == product,
            x.periods == periods
            ]),
            func=lambda name, index, obj: errors.append(obj)
        ).map(lambda x: x.dict())

        delete_query = self._filter(
            provider=provider,
            product=product,
            market=market,
            periods=periods,
            after=after
        )

        deleted, inserted = self.bulk_delete_insert(
            delete_query=delete_query,
            rows=rows,
            auto_commit=False
        )

        if len(errors):
            self.db.rollback()
            raise Exception(str(errors))
        else:
            self.db.commit()

        return common_schema.BulkResult(
            deleted=deleted,
            inserted=inserted,
            errors=errors
        )


class CryptoTradeResult(GenericRepository[models.CryptoTradeResult]):
    pass

