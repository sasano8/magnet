from . import models
from libs.fastapi import GenericRepository


class Dummy(GenericRepository[models.Dummy]):
    pass

