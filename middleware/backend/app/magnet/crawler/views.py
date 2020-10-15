from typing import List, Optional
from . import crud
from magnet import get_db, TemplateView, CommonQuery, default_query
from magnet.vendors import cbv, InferringRouter


router = InferringRouter()

@cbv(router)
class CrawlerView(TemplateView[crud.crawlers]):
    @property
    def rep(self) -> crud.crawlers:
        raise NotImplementedError()

    @router.get("/")
    async def index(self, q: CommonQuery = default_query) -> List[str]:
        mapping = map(lambda key_value: key_value[0], crud.crawlers.list())
        arr = list(mapping)
        return arr
