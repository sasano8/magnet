import functools
from pydantic import BaseModel
from .utils import generate_fastapi_funnel
from libs.inspect import ObjectInfo


def fastapi_funnel(func):
    """
        単一のBaseModel引数を持つ関数・メソッドをfastapiのクエリとして解釈するための関数・メソッドを定義します。
        関数・メソッドは以下のように解釈されます。

        class MyClass(BaseModel):
          name: str
          age: int = Field(alias="generation")

        @model_overload_for_api
        def func(obj: MyClass):
          pass

        ↓

        def wapped(name: str = Query(alias="name"), age: int = Query(alias="generation")):
          func(MyClass(
            name=name,
            age=age
          ))
    """
    info = ObjectInfo(func)
    sig = info.signature

    # TODO: callableでもいいかも
    if not info.is_function:
        raise TypeError(f"{func.__name__} is not function.")

    args = list(sig.parameters.items())
    is_method = info.is_method or info.is_unbounded_method

    if is_method:
        first_arg = args.pop(0)  # cls, selfを除外する

    args_len = len(args)
    if args_len > 1:
        raise TypeError(f"{func.__name__}: 単一の引数にBaseModelを持つ関数でありません。")
    elif args_len == 0:
        raise TypeError(f"{func.__name__}: 単一の引数にBaseModelを持つ関数でありません。")

    key, param = args[0]
    if not issubclass(param.annotation, BaseModel):
        raise TypeError(f"{func.__name__} {key}: BaseModelを継承したクラスでありません。")

    # ここまで共通処理

    instantiate_model = generate_fastapi_funnel(
        cls=param.annotation,
        as_method=is_method
    )

    if info.is_coroutine_function:
        if is_method:
            @functools.wraps(instantiate_model)
            async def wrapper(*args, **kwargs):
                if len(args):
                    self_or_cls = args[0]
                else:
                    # fastapiかfastapi-utilsのせいかなぜかキーワードにselfが渡ってくる
                    self_or_cls = kwargs.pop("self", None)
                    if self_or_cls is None:
                        self_or_cls = kwargs.pop("cls", None)

                model = instantiate_model(self_or_cls, **kwargs)
                return await func(self_or_cls, model)
        else:
            @functools.wraps(instantiate_model)
            async def wrapper(*args, **kwargs):
                model = instantiate_model(**kwargs)
                return await func(model)

    else:
        if is_method:
            @functools.wraps(instantiate_model)
            def wrapper(*args, **kwargs):
                if len(args):
                    self_or_cls = args[0]
                else:
                    # fastapiかfastapi-utilsのせいかなぜかキーワードにselfが渡ってくる
                    self_or_cls = kwargs.pop("self", None)
                    if self_or_cls is None:
                        self_or_cls = kwargs.pop("cls", None)

                model = instantiate_model(self_or_cls, **kwargs)
                return func(self_or_cls, model)
        else:
            @functools.wraps(instantiate_model)
            def wrapper(*args, **kwargs):
                model = instantiate_model(**kwargs)
                return func(model)

    wrapper.interface = wrapper
    wrapper.origin = func
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__qualname__ = func.__qualname__
    if "return" in func.__annotations__:
        wrapper.__annotations__["return"] = func.__annotations__["return"]

    return wrapper


def funnel(func):
    info = ObjectInfo(func)
    sig = info.signature

    # TODO: callableでもいいかも
    if not info.is_function:
        raise TypeError(f"{func.__name__} is not function.")

    args = list(sig.parameters.items())
    is_method = info.is_method or info.is_unbounded_method

    if is_method:
        first_arg = args.pop(0)  # cls, selfを除外する

    args_len = len(args)
    if args_len > 1:
        raise TypeError(f"{func.__name__}: 単一の引数にBaseModelを持つ関数でありません。")
    elif args_len == 0:
        raise TypeError(f"{func.__name__}: 単一の引数にBaseModelを持つ関数でありません。")

    key, param = args[0]
    if not issubclass(param.annotation, BaseModel):
        raise TypeError(f"{func.__name__} {key}: BaseModelを継承したクラスでありません。")

    # ここまで共通処理

    instantiate_model = param.annotation  # BaseModelのコンストラクタ

    if info.is_coroutine_function:
        if is_method:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                if len(args) == 1:
                    args = tuple([args[0], instantiate_model(**kwargs)])
                else:
                    if len(kwargs):
                        raise ValueError("位置限定引数とキーワード限定引数のいずれかのみ受け入れ可能です。")
                return await func(*args)
        else:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                if len(args) == 0:
                    args = tuple([instantiate_model(**kwargs)])
                else:
                    if len(kwargs):
                        raise ValueError("位置限定引数とキーワード限定引数のいずれかのみ受け入れ可能です。")
                return await func(*args)
    else:
        if is_method:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if len(args) == 1:
                    args = tuple([args[0], instantiate_model(**kwargs)])
                else:
                    if len(kwargs):
                        raise ValueError("位置限定引数とキーワード限定引数のいずれかのみ受け入れ可能です。")
                return func(*args)
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if len(args) == 0:
                    args = tuple([instantiate_model(**kwargs)])
                else:
                    if len(kwargs):
                        raise ValueError("位置限定引数とキーワード限定引数のいずれかのみ受け入れ可能です。")
                return func(*args)

    return wrapper

