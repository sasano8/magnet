import logging
from logging import getLogger

from magnet.env import Env

log_setting = Env.logging["default"]
logging.basicConfig(
    level=logging._nameToLevel[log_setting.level],
    datefmt=log_setting.format_date,
    format=log_setting.format_msg
)

logger = getLogger("magnet")

class ORM:
    orm_mode = True
