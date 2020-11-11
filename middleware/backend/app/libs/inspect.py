from dataclasses import dataclass
from typing import Any, Literal
import inspect
import re


@dataclass
class ObjectInfo:
    target: Any

    @property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self.target)

    def get_signature_by_kind(self, kind: Literal["POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD", "VAR_POSITIONAL", "KEYWORD_ONLY", "VAR_KEYWORD"]):
        # POSITIONAL_ONLY = 0  # /より前に定義された引数に対応
        # POSITIONAL_OR_KEYWORD = 1  # 特に指定がない場合の標準的な束縛動作
        # VAR_POSITIONAL = 2  # *argsに対応する  可変長位置限定引数は一度しか定義できない　２回目はinvalid syntaxとなる
        # KEYWORD_ONLY = 3  # *, **args以降に出現する引数
        # VAR_KEYWORD = 4  # **kwargsに対応する　可変長キーワード限定引数は一度しか定義できない　２回目はinvalid syntaxとなる
        return inspect.signature(self.target).parameters.items()

    @property
    def is_instantiated(self) -> bool:
        return isinstance(self.target, self.target.__class__)

    @property
    def is_function(self) -> bool:
        return inspect.isfunction(self.target)

    @property
    def is_coroutine(self) -> bool:
        return inspect.iscoroutine(self.target)

    @property
    def is_coroutine_function(self) -> bool:
        return inspect.iscoroutinefunction(self.target)

    @property
    def is_awaitable(self) -> bool:
        return inspect.isawaitable(self.target)

    @property
    def is_awaitable(self) -> bool:
        return inspect.isawaitable(self.target)

    @property
    def is_generatorfunction(self) -> bool:
        return inspect.isgeneratorfunction(self.target)

    @property
    def is_method(self) -> bool:
        return inspect.ismethod(self.target)

    @property
    def is_static_method(self) -> bool:
        return isinstance(self.target, staticmethod)

    @property
    def is_unbounded_method(self) -> bool:
        """
        第一引数にselfまたはclsを持つ関数をメソッドとして判定する。
        selfとclsの名前は、別名を名付けることができるため、確実に判定できる保証がないが、この方法しかないと思われる。

        インスタンスが作成され、関数がインスタンスにバインドされたfunctionをmethodと呼ぶが、
        inspectモジュールは、クラス定義時におけるメソッドはただのfunctionとして判定するため、
        クラス定義時にis_methodを代替する関数が必要となった。
        """
        if not self.is_function:
            return False

        if self.is_static_method:
            return False
        elif self.is_method:
            return False

        args = list(self.signature.parameters.items())
        if len(args):
            key, value = args[0]
            if key == "self" or key == "cls":
                return True
            else:
                return False
        else:
            return False

    @property
    def is_callable(self) -> bool:
        return callable(self.target)

    @property
    def belong_qual_name(self) -> str:
        """自身を除いた__qualname__を返す"""
        # インスタンスが作成され、関数がインスタンスにバインドされるまではメソッドであるか分からないため、クラスに属した関数かチェックする
        qualname_arr = self.target.__qualname__.split(".")
        del qualname_arr[-1]  # delete last element(self).
        return ".".join(qualname_arr)

    @property
    def is_class_attr(self) -> bool:
        s = self.belong_qual_name
        if s == "":
            return False

        if re.search(r'<locals>', s):
            raise Exception("ローカルスコープのオブジェクトは解析できません")

        return True

