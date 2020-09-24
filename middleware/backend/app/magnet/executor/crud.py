from libs.decorators import Instantiate
from magnet.database import GenericRepository
from . import models

@Instantiate
class Executor(GenericRepository[models.Executor]):
    pass


@Instantiate
class ExecutorJob(GenericRepository[models.ExecutorJob]):
    pass

