from magnet import Base
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr


class TradeProfileBase:
    id = sa.Column(sa.Integer, primary_key=True)
    version = sa.Column(sa.Integer, nullable=False, default=0)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.String(1024), nullable=False)
    provider = sa.Column(sa.String(255), nullable=False)
    market = sa.Column(sa.String(255), nullable=False)
    product = sa.Column(sa.String(255), nullable=False)
    periods = sa.Column(sa.Integer, nullable=False)
    cron = sa.Column(sa.String(255), nullable=False)
    broker = sa.Column(sa.String(255), nullable=False)
    bet_strategy = sa.Column(sa.String(255), nullable=True)
    order_logic = trade_rule = sa.Column(sa.JSON, nullable=True, default={})
    job_type = sa.Column(sa.String(255), nullable=True)
    trade_type = sa.Column(sa.String(255), nullable=False)
    monitor_topic = sa.Column(sa.String(255), nullable=False)
    detector_name = sa.Column(sa.String(255), nullable=False)

    @declared_attr
    def __table_args__(cls):
        return (
            sa.UniqueConstraint("name"),
        )


class TradeProfile(TradeProfileBase, Base):
    __tablename__ = "trade_profile"


class TradeJob(TradeProfileBase, Base):
    __tablename__ = "trade_job"
    last_check_date = sa.Column(sa.DateTime, nullable=True)
    order_status = sa.Column(sa.JSON, nullable=True)



