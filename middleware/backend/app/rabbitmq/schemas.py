import asyncio
from pydantic import BaseModel
from typing import List, Dict, Any, Callable
from fastapi.encoders import jsonable_encoder
import json
from inspect import signature
from enum import Enum
from typing import Dict

class Message(BaseModel):
    func: str
    kwargs: dict



class FunctionWrapper(BaseModel):
    class FuncType(int, Enum):
        NORMAL = 0
        ASYNC = 1
    name: str
    func: Any
    func_type: int
    converters: Dict[str, Any]

    def __init__(self, func_name, func):
        converters = {}
        for key, converter in self.enumrate_arg_converter(func):
            converters[key] = converter

        if asyncio.iscoroutinefunction(func):
            func_type = self.FuncType.ASYNC
        else:
            func_type = self.FuncType.NORMAL

        super().__init__(
            name=func_name,
            func=func,
            func_type=func_type,
            converters=converters
        )


    def enumrate_arg_converter(self, func):
        sig = signature(func)
        for k, t in sig.parameters.items():
            if issubclass(t.annotation, BaseModel):
                yield k, lambda x: t.annotation(**x)
            else:
                pass

    def decode_str_arg(self, json: str):
        dic = json.loads(json)
        return self.decode_json_arg(**dic)

    def decode_json_arg(self, *args, **kwargs):
        # 位置引数をキーワード引数に変換する
        kwargs.update(zip(self.func.__code__.co_varnames, args))

        # 関数の引数にpydantic型があればpydantic型にデコードする
        for key, val in kwargs.items():
            if key in self.converters:
                converter = self.converters[key]
                kwargs[key] = converter(val)

        return kwargs

    def __call__(self, *args, **kwargs):
        return self.func(**kwargs)


    def encode_arg_to_dict(self, args, kwargs):
        # 位置引数をキーワード引数に変換する
        kwargs.update(zip(self.func.__code__.co_varnames, args))
        if len(kwargs):
            data = jsonable_encoder(kwargs)
        else:
            data = jsonable_encoder(kwargs, exclude={"kwargs"})

        return Message(
            func=self.name,
            kwargs=data
        ).dict()


    def encode_arg_to_json(self, args, kwargs):
        dic = self.encode_arg_to_dict(args, kwargs)
        str_json = json.dumps(dic, ensure_ascii=False)
        return str_json


    def decode(self):
        # https://pydantic-docs.helpmanual.io/usage/exporting_models/#json_encoders
        # Custom JSON (de)serialisation
        raise NotImplementedError

