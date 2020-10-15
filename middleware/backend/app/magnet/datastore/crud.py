from . import models, schemas
from libs.decorators import Instantiate
from libs.fastapi import GenericRepository
from sqlalchemy.orm import Session, Query
import datetime
from typing import Iterable, Tuple, List
from libs.linq import Linq
from magnet import schemas as common_schema

@Instantiate
class CryptoOhlcDaily(GenericRepository[models.CryptoBase]):

    def _filter(self, db: Session, provider: str, market: str, product: str, periods: int, after: datetime.datetime) -> Query:
        m = models.CryptoBase

        return self.query(db).filter(
            m.provider == provider,
            m.product == product,
            m.market == market,
            m.periods == periods,
            m.close_time >= after
        )

    def filter(self, db: Session, skip: int = 0, limit: int = 100, provider: str = "cryptowatch", market: str = "bitfllyer", product: str = "bitcjpy", periods: int = 60 * 60 * 24, after: datetime.datetime = datetime.datetime(2010, 1, 1)) -> List[models.CryptoBase]:
        query = self._filter(
            db=db,
            provider=provider,
            product=product,
            market=market,
            periods=periods,
            after=after
        )

        return query.offset(skip).amount(limit).all()

    def bulk_insert_by_laundering(self, db: Session, data: Iterable[schemas.Ohlc], provider: str = "cryptowatch", market: str = "bitfllyer", product: str = "bitcjpy", periods: int = 60 * 60 * 24, after: datetime.datetime = datetime.datetime(2010, 1, 1)) -> common_schema.BulkResult:
        """
        指定した条件のデータを削除した後、指定したデータを登録します。（洗い替え方式）
        戻り地に削除件数と登録件数を返します。
        """
        errors = []
        data = Linq(data).hook_if(lambda x: not all([
            x.provider == provider,
            x.market == market,
            x.product == product,
            x.periods == periods
            ]),
            func=lambda name, index, obj: errors.append(obj)
        )

        delete_query = self._filter(
            db=db,
            provider=provider,
            product=product,
            market=market,
            periods=periods,
            after=after
        )

        deleted, inserted = self.bulk_delete_insert(
            db=db,
            query=delete_query,
            data=data,
            auto_commit=False
        )

        if len(errors):
            db.rollback()
            raise Exception(str(errors))
        else:
            db.commit()

        return common_schema.BulkResult(
            deleted=deleted,
            inserted=inserted,
            errors=errors
        )

