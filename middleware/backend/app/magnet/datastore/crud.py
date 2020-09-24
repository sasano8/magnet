from . import models
from magnet.database import GenericRepository, instantiate


@instantiate
class CryptoOhlcDaily(GenericRepository[models.CryptoOhlcDaily]):
    pass