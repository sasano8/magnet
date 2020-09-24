from . import models
from magnet.database import GenericRepository
from libs.decorators import Instantiate

@Instantiate
class Casenode(GenericRepository[models.CaseNode]):
    pass


@Instantiate
class Target(GenericRepository[models.Target]):
    pass
