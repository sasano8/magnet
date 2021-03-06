import asyncio
import datetime
from typing import List, Literal, Union
from fastapi import Query, Body, status
from magnet import get_db, Session, PagenationQuery, Depends, HTTPException, Env, BaseModel, logger
from magnet.vendors import cbv, InferringRouter, TemplateView, build_exception, fastapi_funnel
from . import crud, schemas, models, algorithms
# from magnet.trader_broker import interface
from .core import interfaces
# from magnet.trader_broker.crud import brokers
from magnet.trader.crud import brokers
from magnet.trader import etl

router = InferringRouter()


@cbv(router)
class TradeProfileView(TemplateView[crud.TradeProfile]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.TradeProfile:
        return super().rep

    @router.get("/template")
    @fastapi_funnel
    async def index(self, q: PagenationQuery) -> List[schemas.TradeProfile]:
        return super().index(skip=q.skip, limit=q.limit)

    @router.post("/template")
    async def create(self, data: schemas.TradeProfileCreate) -> schemas.TradeProfile:
        obj = self.rep.get_by_name(data.name)
        if obj:
            e = build_exception(
                status_code=422,
                loc=("name",),
                msg="すでに同名のテンプレートが存在します。",
            )
            raise e
        return super().create(data=data)

    @router.get("/template/{id}")
    async def get(self, id: int) -> schemas.TradeProfile:
        return super().get(id=id)

    @router.delete("/template/{id}/delete", status_code=200)
    async def delete(self, id: int) -> int:
        return super().delete(id=id)

    @router.patch("/template/{id}/patch")
    async def patch(self, id: int, data: schemas.TradeProfilePatch) -> schemas.TradeProfile:
        return super().patch(id=id, data=data)

    # @router.post("/template/{id}/copy")
    # async def copy(self, id: int) -> schemas.TradeProfile:
    #     return super().duplicate(id=id)

    @router.post("/template/{id}/copy_as_worker")
    async def copy_as_worker(self, id: int, as_job_name: str, as_job_type: Literal["production", "virtual", "backtest"]) -> schemas.TradeJob:
        job_view = TradeJobView(db=self.db)
        obj = await self.get(id=id)
        job = schemas.TradeJob.from_orm(obj)
        job.id = None
        job.name = as_job_name
        job.job_type = as_job_type
        created = await job_view.create(data=job)
        return created


@cbv(router)
class TradeJobView(TemplateView[crud.TradeJob]):
    db: Session = Depends(get_db)

    @property
    def rep(self) -> crud.TradeJob:
        return super().rep

    @router.get("/worker")
    @fastapi_funnel
    async def index(self, q: PagenationQuery) -> List[schemas.TradeJob]:
        return super().index(skip=q.skip, limit=q.limit)

    @router.post("/worker")
    async def create(self, data: schemas.TradeProfileCreate) -> schemas.TradeJob:
        obj = self.rep.get_by_name(data.name)
        if obj:
            e = build_exception(
                status_code=422,
                loc=("name",),
                msg="すでに同名のテンプレートが存在します。",
            )
            raise e
        data.order_status = None
        return super().create(data=data)

    @router.get("/worker/{id}")
    async def get(self, id: int) -> schemas.TradeJob:
        return super().get(id=id)

    @router.delete("/worker/{id}/delete", status_code=200)
    async def delete(self, id: int) -> int:
        return super().delete(id=id)

    @router.patch("/worker/{id}/patch")
    async def patch(self, id: int, data: schemas.TradeProfilePatch) -> schemas.TradeJob:
        return super().patch(id=id, data=data)

    # @router.post("/job/{id}/copy")
    # async def copy(self, id: int) -> schemas.TradeJob:
    #     result = self.rep.duplicate(id=id)
    #     if result is None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #
    #     return result

    @router.post("/worker/{id}/reset_order_status")
    async def reset_order_status(self, id: int) -> schemas.TradeJob:
        obj = await self.get(id=id)
        data = schemas.TradeJob.from_orm(obj)
        data.order_status = None
        data.last_check_date = None
        return await self.patch(id=id, data=data)

    @router.post("/worker/{id}/exec")
    async def exec(self, id: int):
        """ジョブを実行する。last_check_dateからさかのぼってエントリーを行う。Noneの場合は、本日分よりトレードを行う。"""
        tmp = await self.get(id=id)
        job = schemas.TradeJob.from_orm(tmp)

        import magnet.datastore.crud
        ohlc = magnet.datastore.crud.CryptoOhlcDaily(self.db)
        rep_result = crud.TradeResult(self.db)
        scheduler = []

        def create_schedule(before, until):
            if before > until:
                raise Exception()

            diff = (until - before).days
            start_day = datetime.date.today() - datetime.timedelta(days=diff)
            for day_count in range(diff):
                yield start_day + datetime.timedelta(days=day_count)

        if job.job_type == "production":
            broker = brokers.instatiate(job.broker)
            broker.sleep_interval = 10
            if job.last_check_date is None:
                scheduler = list(create_schedule(datetime.date.today(), datetime.date.today()))
            else:
                scheduler = list(create_schedule(job.last_check_date.date(), datetime.date.today()))
        elif job.job_type == "virtual":
            # 現在に対して仮想的にトレードを行う
            broker = brokers.instatiate(job.broker)
            broker.sleep_interval = 10
            broker = broker  # 仮想ブローカーにラップする
            if job.last_check_date is None:
                current_date = datetime.datetime.now().date() - datetime.timedelta(days=1)  # 本日はすなわち昨日のクローズタイム - 1日
                scheduler = [datetime.date.today()]
            raise NotImplementedError()
        elif job.job_type == "backtest":
            # 過去データに対してトレードを行う
            job = await self.reset_order_status(id=job.id)
            job = schemas.TradeJob.from_orm(job)
            rep_result.delete_by_job_name(job.name)
            broker = brokers.instatiate("backtest")
            broker.sleep_interval = 0  # 外部との通信はないので0
            query = ohlc.select_close_date(
                provider=job.provider,
                market=job.market,
                product=job.product,
                periods=job.periods,
                until=datetime.date.today(),
                order_by="asc"
            )
            scheduler = [datetime.datetime.combine(x.close_time, datetime.time()) for x in query][:-1]
            logger.info(f"{len(scheduler)}件のデータでバックテストを行います。")
        else:
            raise Exception()

        # broker.get_topic
        # broker.scheduler = scheduler
        # broker.trade_type = None
        broker.db = self.db
        broker.detect_signal = algorithms.detectors.get(job.detector_name)

        for dt in scheduler:
            # ジョブを更新しないと状態が更新されない
            # tmp = await self.get(id=id)
            # job = schemas.TradeJob.from_orm(tmp)
            job = await self.stop_and_reverse(job, broker, dt)

        return job

    async def stop_and_reverse(self, job, broker, close_time_or_every_second) -> schemas.TradeJob:
        """ドテン方式アルゴリズムを実行する"""
        check = broker.valid_currency_pair(job.product)  # 念の為有効なプロダクト名か確認

        today = close_time_or_every_second + datetime.timedelta(days=1)

        # 最新データがあるか確認
        today_topic = await broker.get_topic(self.db, job, today)
        if not today_topic:
            logger.warning(f"{today}のデータがありません。")
            return job

        # 昨日分のデータを取得
        topic = await broker.get_topic(self.db, job, close_time_or_every_second)

        # topic.t_cross = 1  # mock test
        limit_or_loss = job.detect_limit_loss(today_topic.close_price)
        if limit_or_loss:
            if job.order_status:
                if job.order_status.status == "entried":
                    job = await broker.order("settle", job, today, self.db)
                    await broker.notify(limit_or_loss, close_time_or_every_second)

                if job.order_status and job.order_status.status == "settled":
                    retry_count = 5
                    for i in range(retry_count):
                        await asyncio.sleep(broker.sleep_interval)  # 注文直後は証拠金や注文がが更新されていないため、少し時間を開ける
                        entry_order = await broker.fetch_order_result(job.order_status.entry_order)
                        settle_order = await broker.fetch_order_result(job.order_status.settle_order)
                        if (entry_order is None or settle_order is None) == False:
                            break

                    job.order_status.entry_order = entry_order
                    job.order_status.settle_order = settle_order

                    # トレード結果を保存
                    rep_result = crud.TradeResult(self.db)
                    rep_result.create_from_job(job)

                    job.order_status = None
                    await self.patch(id=job.id, data=job)

        # サイン検出
        bid_or_ask = broker.detect_signal(topic)
        if bid_or_ask is None:
            return await broker.order("pass", job, today, self.db)  # 最終チェック日を更新

        if job.order_status:
            if job.order_status.status == "entried":
                job = await broker.order("settle", job, today, self.db)

        if job.order_status and job.order_status.status == "settled":
            retry_count = 5
            for i in range(retry_count):
                await asyncio.sleep(broker.sleep_interval)  # 注文直後は証拠金や注文がが更新されていないため、少し時間を開ける
                entry_order = await broker.fetch_order_result(job.order_status.entry_order)
                settle_order = await broker.fetch_order_result(job.order_status.settle_order)
                if (entry_order is None or settle_order is None) == False:
                    break

            job.order_status.entry_order = entry_order
            job.order_status.settle_order = settle_order

            # トレード結果を保存
            rep_result = crud.TradeResult(self.db)
            rep_result.create_from_job(job)

            job.order_status = None
            await self.patch(id=job.id, data=job)

        # 発注済みなら実行しない
        if job.order_status and job.order_status.status == "entried":
            return await broker.order("pass", job, today, self.db)  # 最終チェック日を更新

        current_price = topic.close_price
        # current_price = broker.get_ticker()

        entry_order = interfaces.Order(
            bid_or_ask=bid_or_ask,
            order_type="market",
            time_in_force="GTC",
            currency_pair=job.product,
            # price=profile.trade_rule.entry,
            amount=job.calc_amount(current_price),
            limit=job.calc_limit(bid_or_ask, current_price),
            loss=job.calc_loss(bid_or_ask, current_price),
            comment="cross"
        )
        # 決済用注文
        settle_order = interfaces.OrderStatus.create_settle_order(entry_order)

        job.order_status = interfaces.OrderStatus(
            entry_order=entry_order,
            settle_order=settle_order,
        )

        # 新規注文
        return await broker.order("entry", job, today, self.db)


@cbv(router)
class Etl:
    db: Session = Depends(get_db)

    @router.post("/etl/load_all")
    async def load_all(self):
        all_result = {}
        result = await self.load_pairs()
        all_result["load_pairs"] = result

        result = await self.load_ohlc()
        all_result["load_ohlc"] = result

        return all_result

    @router.post("/etl/load_pairs")
    async def load_pairs(self):
        return await etl.load_pairs(self.db)

    @router.post("/etl/load_ohlc")
    async def load_ohlc(self):
        return await etl.load_ohlc(self.db)


