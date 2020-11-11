import functools
from typing import Type, Literal
from pydantic import BaseModel


# TODO: モデルの作成まではやらずに辞書を作るところまでに抽象化すれば処理を共通化できるのでは
def generate_func_code(cls: Type[BaseModel], as_method=False):
    bind_func_name = "tmp_func"
    bind_model_name = "Model"

    annotations = {}
    defaults = []
    kwdefaults = {}

    fields_required = []
    fields_non_required = []

    # sort required first
    for field in cls.__fields__.values():
        if field.required:
            fields_required.append(field)
        else:
            fields_non_required.append(field)

    fields = fields_required
    fields += fields_non_required

    for field in fields:
        annotations[field.name] = field.type_
        if not field.required:
            kwdefaults[field.name] = field.default

    if as_method:
        codes = [f"def {bind_func_name}(self, *,"]
    else:
        codes = [f"def {bind_func_name}(*,"]

    # definition kwargs.
    for field in fields:
        if field.required:
            codes.append(f"  {field.name},")
        else:
            codes.append(f"  {field.name}=None,")

    codes.append("):")
    codes.append(f"  return {bind_model_name}(")

    # create instance
    for field in fields:
        codes.append(f"    {field.name}={field.name},")

    codes.append("  )")
    code = "\n".join(codes)
    return code, bind_func_name, bind_model_name, annotations, tuple(defaults), kwdefaults


def generate_funnel(cls: Type[BaseModel], as_method=False):
    """
    pydantic BaseModelで定義した属性を引数とするコンストラクタ関数を作成する。
    """
    code, bind_func_name, bind_model_name, annotations, defaults, kwdefaults = generate_func_code(
        cls,
        as_method
    )
    local_namespace = {bind_func_name: None, bind_model_name: cls}
    exec(code, local_namespace, local_namespace)
    func = local_namespace[bind_func_name]
    func.__annotations__ = annotations  # 引数に型を付与
    # func.__defaults__  # 位置引数のデフォルトを定義  # POSITIONAL_OR_KEYWORDの場合は、defaultsに定義される
    func.__kwdefaults__ = kwdefaults  # デフォルト値を定義
    return func


def generate_fastapi_funnel(cls: Type[BaseModel], as_method=False):
    func = generate_funnel(cls=cls, as_method=as_method)
    queries = get_queries(cls)
    # func.__defaults__  # 位置引数のデフォルトを定義  # POSITIONAL_OR_KEYWORDの場合は、defaultsに定義される
    func.__kwdefaults__ = queries
    return func


def get_queries(cls: Type[BaseModel]) -> dict:
    from pydantic import Field
    from fastapi import Query

    result = {}

    for k, v in cls.__fields__.items():
        field = cls.__fields__[k]
        if field.required:
            query = Query(..., alias=field.alias)
        else:
            query = Query(field.default, alias=field.alias)

        result[k] = query

    return result