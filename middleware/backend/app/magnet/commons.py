from typing import List, Union, Literal, Dict
from libs.pydantic import BaseModel


class BaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True  # エイリアス名でデータを入力できる
        allow_mutation = True  # イミュータブルだと利便性が悪いため、ミュータブルとする
        extra = "forbid"  # 追加属性を禁止
        # underscore_attrs_are_private = True  先頭アンダースコア一つはプライベートとして扱う


class PagenationQuery(BaseModel):
    skip: int = 0
    limit: int = 100
    _kwargs: Dict[Literal["aa", "b", "c"], str] = {}
    class Config:
        fields = {
            "skip": "from",
        }
