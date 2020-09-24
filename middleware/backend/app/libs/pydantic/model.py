from pydantic import BaseModel

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


class BaseConfig:
        fields = alias_min
        allow_population_by_field_name = True  # インスタンス生成時のパラメータを、# フィールド名・エイリアスの両対応とする


class Base(BaseModel):
    class Config(BaseConfig):
        pass
