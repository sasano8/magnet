from typing import Optional
from fastapi import FastAPI, APIRouter, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Union, Literal


class BaseModel(BaseModel):
    class Config:
        allow_mutation = False  # インスタンス生成後の変更を禁止
        extra = "forbid"  # 追加属性を禁止

    @classmethod
    def new_type(cls, suffix):
        return type(
            cls.__name__ + suffix,
            (cls,),
            {}
        )

    @classmethod
    def prefab(cls, suffix, exclude: tuple = (), requires: tuple = (), optionals: tuple = None):
        """
        出力するフィールドを制限し、指定されたフィールドの必須・オプション属性を更新した新しいスキーマクラスを生成する。
        optionals = None : フィールドのオプション属性を引き継ぐ
        optionals = [...] : 全てのフィールドをオプションにする。
        optionals = ["field1", "field2"] : 指定したフィールドをオプションにする
        """
        new_type = cls.new_type(suffix)

        if optionals is None:
            optionals = ()

        if len(optionals) == 1 and optionals[0] is ...:
            optionals = new_type.__fields__.keys()

        # 指定されたフィールドをオプションにする
        for key in optionals:
            new_type.__fields__[key].required = False

        # 指定されたフィールドを除外する
        for item in exclude:
            del new_type.__fields__[item]
            # if item in new_type.__fields_set__:  # エイリアスなど拡張属性が格納されてるっぽい
            #     del new_type.__fields_set__
            new_type.__field_defaults__.pop(item, None)
            # new_type.__validators__

        # 指定されたフィールドを必須にする
        for item in requires:
            new_type.__fields__[item].required = True

        return new_type


class Condition(BaseModel):
    field: str
    op: Literal["==", "!="]
    condition: str


class ConditionOrAnd(BaseModel):
    op: Literal["and", "or"]
    conditions: List[Condition] = []


class CommonQuery(BaseModel):
    skip: int = Field(0, alias="from")
    limit: int = 100
    query: str = None
    # sort_by: List[str] = Field(None, alias="sortBy"),


async def common_page_query(skip: int = Query(0, alias="from"), limit: int = 100) -> CommonQuery:
    return CommonQuery(skip=skip, limit=limit)


default_paginate: CommonQuery = Depends(common_page_query)
default_query: CommonQuery = Depends(CommonQuery)
