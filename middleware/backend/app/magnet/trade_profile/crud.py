from magnet import GenericRepository
from . import models


class TradeProfile(GenericRepository[models.TradeProfile]):
    def get_by_name(self, name: str):
        return self.query().filter(models.TradeProfile.name == name).one_or_none()


class TradeJob(GenericRepository[models.TradeJob]):
    def get_by_name(self, name: str):
        return self.query().filter(models.TradeJob.name == name).one_or_none()
