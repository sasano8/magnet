import functools
import itertools
# import statistics
import numpy
import itertools
from typing import Callable, Any


def linq(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        query = Linq(iteratable=result)
        # query.func_name = func.__name__
        return query
    return wrapper


class Linq:
    def __init__(self, iteratable):
        if not hasattr(iteratable, "__iter__"):
            raise TypeError(f"{type(iteratable)} object is not iteratable")

        self.__iteratable = iteratable

        if isinstance(iteratable, Linq):
            self.__previous = self.__iteratable

    def __iter__(self):
        return self.__iteratable.__iter__()

    @linq
    def filter(self, func) -> 'Linq':
        return filter(func, self)

    @linq
    def of_type(self, typ) -> 'Linq':
        if typ is None:
            typ = None.__class__

        return filter(lambda x: isinstance(x, typ), self)

    @linq
    def of_ignore_type(self, typ):
        if typ is None:
            typ = None.__class__

        return filter(lambda x: not isinstance(x, typ), self)

    @linq
    def distinct(self) -> 'Linq':
        raise NotImplementedError()

    @linq
    def take(self, count) -> 'Linq':
        def wrap(iterator):
            return filter(lambda tupple: tupple[0] % count == 0, enumerate(iterator))
        return wrap(self)

    @linq
    def skip(self, count) -> 'Linq':
        raise NotImplementedError()

    @linq
    def take_while(self, func) -> 'Linq':
        return itertools.takewhile(func, self)

    @linq
    def drop_while(self, func) -> 'Linq':
        return itertools.dropwhile(func, self)

    @linq
    def take_until(self, func) -> 'Linq':
        # take_until(obj == True) = > drop_while(obj == False)
        raise NotImplementedError()

    @linq
    def drop_until(self, func) -> 'Linq':
        raise NotImplementedError()

    @linq
    def even(self) -> 'Linq':
        return filter(lambda x: x % 2 == 0, self)

    @linq
    def odd(self) -> 'Linq':
        return filter(lambda x: x % 2 != 0, self)

    @linq
    def select(self, func) -> 'Linq':
        return map(func, self)

    @linq
    def cast(self, type) -> 'Linq':
        raise NotImplementedError()

    @linq
    def select_many(self, func) -> 'Linq':
        raise NotImplementedError()

    @linq
    def lookup(self, key_selector):
        """指定されたキー セレクター関数および要素セレクター関数に従って、Lookup<TKey,TElement> から IEnumerable<T> を作成します。"""
        # var result = dictionary.ToLookup(item => item.Value[0], item => item.Key);
        raise NotImplementedError()

    @linq
    def group_by(self, func):
        raise NotImplementedError()

    @linq
    def default_if_empty(self):
        raise NotImplementedError()

    # joinとの違いは何？
    @linq
    def concat(self, iterable) -> 'Linq':
        raise NotImplementedError()

    @linq
    def join(self, iterable) -> 'Linq':
        raise NotImplementedError()

    @linq
    def group_join(self) -> 'Linq':
        raise NotImplementedError()

    @linq
    def reverse(self) -> 'Linq':
        raise NotImplementedError()
        # return reversed(self) # listを返すので関数を返したい

    @linq
    def order_by_asc(self, func) -> 'Linq':
        raise NotImplementedError()
        # sort 元のリストを破壊的にソート
        # sorted ソートした新たなリストを生成
        # どちらもlistを返すのでクエリを返したい
        # import heapq

    @linq
    def order_by_desc(self, func) -> 'Linq':
        raise NotImplementedError()

    @linq
    def then_by_asc(self) -> 'Linq':
        raise NotImplementedError()

    @linq
    def then_by_desc(self) -> 'Linq':
        raise NotImplementedError()

    @linq
    def union(self) -> 'Linq':
        raise NotImplementedError()

    # except
    @linq
    def difference(self) -> 'Linq':
        raise NotImplementedError()

    @linq
    def intersect(self) -> 'Linq':
        raise NotImplementedError()

    # 単一要素取得
    def element_at(self, index):
        # return self.__iteratable.__getitem__(index)
        raise NotImplementedError()

    def element_at_or_default(self):
        raise NotImplementedError()

    def one_or_none(self):
        result = None
        for index, item in enumerate(self):
            if index == 0:
                result = item
            if index > 0:
                raise Exception("not one.")
            break

        return result

    def one(self):
        result = self.one_or_none()
        if result is None:
            raise Exception("not exist.")

        return result

    def one_or_default(self):
        raise NotImplementedError()

    def first_or_none(self):
        result = None
        for index, item in enumerate(self):
            if index == 0:
                result = item
            break

        return result

    def first(self):
        result = self.first_or_none()
        if result is None:
            raise Exception("not exist.")

        return result

    def first_or_default(self):
        raise NotImplementedError()

    def last_or_none(self):
        result = None
        for item in self:
            result = item

        return result

    def last(self):
        result = self.first_or_none()
        if result is None:
            raise Exception("not exist.")

        return result

    def last_or_default(self):
        raise NotImplementedError()

    # 判定
    def contains(self):
        raise NotImplementedError()

    def all(self):
        return all(self)

    def any(self):
        return any(self)

    def sequence_equal(self):
        raise NotImplementedError()

    # 統計
    def count(self) -> int:
        return len(self)

    def max(self) -> float:
        # return max(self, *, default="obj", key="func")
        return max(self)

    def min(self) -> float:
        return min(self)

    def sum(self, start: int = 0) -> float:
        return sum(self, start)

    def avarage(self) -> float:
        return numpy.mean(self)

    def aggregate(self):
        raise NotImplementedError()

    def accumulate(self):
        f = itertools.accumulate
        raise NotImplementedError()

    # 処理実行
    def dispatch(self, func) -> 'Linq':
        """ファンクションに要素を送出します。"""
        for item in self:
            func(item)

        return self

    # オブジェクト化
    def list(self):
        return list(self)

    def tupple(self):
        raise NotImplementedError()

    def dict(self, key_selector):
        raise NotImplementedError()

    def numpy(self):
        raise NotImplementedError()

    def pandas(self):
        raise NotImplementedError()

    def save(self) -> 'Linq':
        """クエリ実行結果を持つ新たなLinqインスタンスを返します。"""
        obj = self.__class__(self.list())
        return obj

    def query(self, iteratable):
        """新しいイテレータを始発点とするクエリのコピーを作成する。"""
        current = self
        names = []
        while current is not None:
            if hasattr(current, "__iteratable"):
                names.append(current.func_name)
                current = current.__iteratable
            else:
                current = None

        names = reversed(names)

        # 難しい
        # selfをラッパーから分離しないとクエリの際限ができない

    @staticmethod
    def empty(cls, iter_type: type = list) -> 'Linq':
        return cls(iter_type())

    @staticmethod
    def range(cls, stop: int, start: int = 0, step: int = 1) -> 'Linq':
        return cls(range(start=start, stop=stop, step=step))

    @staticmethod
    def infinite(cls, func: Callable = lambda: 0) -> 'Linq':
        # generatorがきたらどう処理すべきか？
        def create_iterator():
            while True:
                yield func()
        return cls(create_iterator())


class EmpLinq(Linq):
    def dummy(self):
        # 自身をラップしたジェネレータを保持すると、クエリのみをコピーできない。
        # 基礎となるインスタンスを分離することでクエリのみをコピーすることができる
        func = lambda x: x
        query = functools.partial(filter, func)

        query([])


    def copy(self) -> 'Linq':
        current = self.__previous

        while current:
            current = self.__previous

        if current is None:
            raise Exception("はじめのチェーンでコピーしてもいみなくね")


def lazymerge(a, b):
    s = object() # Sentinel.
    a = iter(a); b = iter(b)
    na = next(a, s); nb = next(b, s)
    while na is not s and nb is not s:
        if na < nb: yield na; na = next(a, s)
        else: yield nb; nb = next(b, s)
    if na is not s: yield na; yield from a
    if nb is not s: yield nb; yield from b

def lazymergesort(l, s=None, e=None):
    if s is None: s = 0; e = len(l)
    if e-s == 1: yield l[s]
    elif e-s > 1: yield from lazymerge(lazymergesort(l, s, s+(e-s)//2),
                                       lazymergesort(l, s+(e-s)//2, e))