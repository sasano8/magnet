from typing import Iterable, Type, TypeVar, Any
from pydantic import BaseModel
from .utils import generate_funnel, generate_func_code

alias_all = {
    "False_": "False",
    "None_": "None",
    "True_": "True",
    "and_": "and",
    "as_": "as",
    "assert_": "assert",
    "break_": "break",
    "class_": "class",
    "continue_": "continue",
    "def_": "def",
    "del_": "del",
    "elif_": "elif",
    "else_": "else",
    "except_": "except",
    "finally_": "finally",
    "for_": "for",
    "from_": "from",
    "global_": "global",
    "if_": "if",
    "import_": "import",
    "in_": "in",
    "is_": "is",
    "lambda_": "lamdba",
    "nonlocal_": "nonlocal",
    "not_": "not",
    "or_": "or",
    "pass_": "pass",
    "raise_": "raise",
    "return_": "return",
    "try_": "try",
    "while_": "while",
    "with_": "with",
    "yield_": "yield"
}

alias_min = {
    "from_": "from",
    "class_": "class",
    "return_": "return",
    "global_": "global",
}

Model = TypeVar('Model', bound='BaseModel')


class BaseConfig:
        fields = alias_min
        allow_population_by_field_name = True  # インスタンス生成時のパラメータを、# フィールド名・エイリアスの両対応とする


# noinspection PyTypeChecker
class BaseModel(BaseModel):
    @classmethod
    def from_orm_query(cls: Type['Model'], query: Iterable[Any]) -> Iterable['Model']:
        for item in query:
            yield cls.from_orm(item)

    @classmethod
    def from_orm_query_as_dict(cls: Type['Model'], query: Iterable[Any]) -> Iterable[dict]:
        for item in cls.from_orm_query(query):
            yield item.dict()

    @classmethod
    def new_type(cls: Type['Model'], suffix) -> Type['Model']:
        return type(
            cls.__name__ + suffix,
            (cls,),
            {}
        )

    @classmethod
    def prefab(cls: Type['Model'], suffix, exclude: tuple = (), requires: tuple = (), optionals: tuple = None) -> Type['Model']:
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

    @classmethod
    def as_func(cls):
        """
        モデル属性を関数の引数にマップした関数を生成します。
        これは、fastapiがpydanticをクエリとして理解しないため、関数に変換しクエリとして解釈されるように利便性を高めるために定義しました。
        モデルは以下のように解釈されます。

        class A(BaseModel):
          name: str
          age: int = 20

        def create_A(name: str, age: int = 20):
            return A(name=name, age=age)
        """
        return generate_funnel(cls)

