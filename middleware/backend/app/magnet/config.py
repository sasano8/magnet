from magnet.env import Env
from rabbitmq import RabbitApp

SQLALCHEMY_DATABASE_URL = Env.databases["default"].get_connection_string()
print(Env.databases["default"])


# loggingの上級チュートリアルの購読を推奨
# https://docs.python.org/ja/3/howto/logging.html#logging-advanced-tutorial
# ハンドラはログの送信先を定義
# フィルタはログの抑制などを司る
# LogRecordインスタンスが、logger, handler, filter, formatter間でやりとりされている。

import logging
from logging import getLogger

# LOG_FORMAT_DATE = '%Y-%m-%d %H:%M:%S'
# LOG_FORMAT_MSG = '%(levelname)s: %(asctime)s %(module)s %(funcName)s %(lineno)d: %(message)s'

# logging.basicConfig(
#     level=logging.INFO,
#     datefmt=LOG_FORMAT_DATE,
#     format=LOG_FORMAT_MSG
# )

log_setting = Env.logging["default"]
logging.basicConfig(
    level=logging._nameToLevel[log_setting.level],
    datefmt=log_setting.format_date,
    format=log_setting.format_msg
)



getLogger = getLogger

rabbitmq = Env.queues["default"]
mq = rabbitmq
# rabbitmq = RabbitApp(
#     broker_url=mq.broker_url,
#     queue_name=mq.queue_name,
#     auto_ack=mq.auto_ack,
#     durable=mq.durable,
#     queue_delete=mq.queue_delete,
# )

class ORM:
    orm_mode = True
