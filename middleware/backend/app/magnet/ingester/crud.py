from . import models
from libs.decorators import Instantiate
from magnet.database import GenericRepository


@Instantiate
class IngesterJobGroup(GenericRepository[models.IngesterJobGroup]):
    pass


@Instantiate
class IngesterJob(GenericRepository[models.IngesterJob]):
    pass


@Instantiate
class Ingester(GenericRepository[models.Ingester]):
    pass

