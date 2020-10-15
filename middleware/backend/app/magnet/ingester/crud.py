from . import models
from libs.fastapi import GenericRepository


class IngesterJobGroup(GenericRepository[models.IngesterJobGroup]):
    pass


class IngesterJob(GenericRepository[models.IngesterJob]):
    pass


class Ingester(GenericRepository[models.Ingester]):
    pass

