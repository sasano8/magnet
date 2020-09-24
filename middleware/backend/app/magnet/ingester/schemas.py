from typing import List, Optional, Any
from pydantic import BaseModel, Json

class ORM:
    orm_mode = True


class Detail(BaseModel):
    url: Optional[str]
    url_cache: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    class Config:
        extra = "allow"

class CommonDimension(BaseModel):
    job_id: int
    user_id: int
    folder_id: int
    project_id: int
    pipeline_id: int


class JobGroupCreate(BaseModel):
    id: Optional[int] = 0
    description: str = ""
    is_system: bool = False


class TaskCreate(BaseModel):
    pipeline_name: str = "postgress"
    crawler_name: str
    keyword: str
    option_keywords: List[Any] = []
    deps: int = 0

    # openapi上でデフォルト値は認識されないため、サンプルを明示的に定義する
    class Config:
        schema_extra = {
            "example": {
                "pipeline_name": "postgres",
                "crawler_name": "scrape_google",
                "keyword": "山田太郎",
            }
        }


class JobCreate(BaseModel):
    jobgroup_id: Optional[int] = 0
    pipeline_name: str = "postgress"
    crawler_name: str
    keyword: str
    option_keywords: List[Any] = []
    deps: int = 0

    # openapi上でデフォルト値は認識されないため、サンプルを明示的に定義する
    class Config:
        schema_extra = {
            "example": {
                "pipeline_name": "postgres",
                "crawler_name": "scrape_google",
                "keyword": "山田太郎",
                "option_keywords": []
            }
        }



class CommonSchema(TaskCreate):
    # Config = ORM
    class Config:
        orm_mode = True

    # pipeline: str
    # crawler_name: str
    # keyword: str
    # option_keywords: List[str] = []
    # deps: int = 0
    referer: Optional[str]
    url: Optional[str]
    url_cache: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    current_page_num: int = 0
    detail: Detail = Detail()

    def copy_summary(self):
        dic = self.dict(exclude={"detail"})
        obj = self.__class__.construct(**dic)
        return obj

    def sync_summary_from_detail(self):
        self.url = self.detail.url
        self.url_cache = self.detail.url_cache
        self.title = self.detail.title
        self.summary = self.detail.summary

