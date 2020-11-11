from typing import Literal
from magnet import GenericRepository
from . import models
import magnet.datastore.crud
import magnet.datastore.schemas
from . import schemas


class TradeProfile(GenericRepository[models.TradeProfile]):
    def get_by_name(self, name: str) -> models.TradeProfile:
        return self.query().filter(models.TradeProfile.name == name).one_or_none()

class TradeJob(GenericRepository[models.TradeJob]):
    def get_by_name(self, name: str) -> models.TradeJob:
        return self.query().filter(models.TradeJob.name == name).one_or_none()


class TradeResult(magnet.datastore.crud.CryptoTradeResult):
    def create_from_job(self, job: schemas.TradeJob):
        obj = convert_job_to_result(job, as_back_test=False)
        created = self.create(data=obj)
        return created

    def get_as_job(self, id: int) -> schemas.TradeJob:
        raise NotImplementedError()

    def delete_by_job_name(self, job_name: str):
        count = self.filter(
            self.model.job_name == job_name
        ).delete()
        self.db.commit()
        return count


def convert_job_to_result(job: schemas.TradeJob, as_back_test: bool = False) -> magnet.datastore.schemas.CryptoTradeResult:
    obj = magnet.datastore.schemas.CryptoTradeResult(
        provider=job.provider,
        market=job.market,
        product=job.product,
        periods=job.periods,
        size=job.order_status.entry_order.amount,
        entry_date=job.order_status.entry_order.order_date,
        entry_side=job.order_status.entry_order.bid_or_ask,
        entry_price=job.order_status.entry_order.price,
        entry_commission=job.order_status.entry_order.commission,
        entry_reason=job.order_status.entry_order.comment,
        settle_date=job.order_status.settle_order.order_date,
        settle_side=job.order_status.settle_order.bid_or_ask,
        settle_price=job.order_status.settle_order.price,
        settle_commission=job.order_status.settle_order.commission,
        settle_reason=job.order_status.settle_order.comment,
        job_name=job.name,
        job_version=job.version,
        is_back_test=as_back_test
    )
    return obj


def convert_result_to_job(trade_result: magnet.datastore.schemas.CryptoTradeResult) -> schemas.TradeJob:
    """どこまで戻せるか？？"""
    raise NotImplementedError()

