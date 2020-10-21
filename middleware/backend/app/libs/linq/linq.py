import functools
import itertools
import operator
# import statistics
import numpy
import itertools
from typing import Callable, Any, TypeVar, Iterable, Generic, Generator, NoReturn, Type, Union, Optional, List, Iterator, Mapping, Dict
import pandas as pd
from pydantic import BaseModel, parse_obj_as, validator
from pydantic.generics import GenericModel
from pydantic.main import ModelMetaclass
from pydantic.tools import NameFactory
import inspect


# https://docs.python.org/ja/3.5/library/collections.abc.html

class Undefined():
    pass


undefined = Undefined()


def linq(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        query = Linq(iterable=result)
        return query
    return wrapper


T = TypeVar('T')
R = TypeVar('R')


def create_query(func, *args, self_pos=-1):
    partial = functools.partial(func, *args)
    return Query(partial, self_pos)


class Query():
    def __init__(self, func: Callable[[], Generator], self_index):
        self.create_iterator = func
        self._self_index = self_index

    def __iter__(self):
        return self.create_iterator()

    @property
    def self_index(self):
        return self._self_index

    @property
    def func(self):
        return self.create_iterator.func

    @property
    def args(self):
        return self.create_iterator.args

    def copy_args(self, target):
        import copy
        args = copy.copy(self.args)
        if self.self_index >= 0:
            args[self.self_index] = target
        return args


class GeneratorWrapper(BaseModel):
    func: Callable

    def __iter__(self):
        return self.func()


def convert_to_queryable(v):
    # 読み出し順は変えないこと
    if isinstance(v, Query):
        return v
    elif isinstance(v, dict):
        query = Linq([])
        query.__root__ = v
        return query._items()
    elif isinstance(v, Iterator):
        return v
    elif isinstance(v, Iterable):
        return v
    elif inspect.isgeneratorfunction(v):
        return GeneratorWrapper(func=v)
    elif hasattr(v, "__getitem__"):  # __getitem__はiterableであるが、isinstanceで判定不可
        return v
    # elif isinstance(v, functools.partial):
    #     partial = functools.partial(filter, lambda x: True, [1, 2])
    #     print(isinstance(partial, functools.partial))
    #     print(issubclass(partial.func, Iterable))
    #     callable = (
    #       Linq([v])
    #       .select_recursive(lambda x: x.func)
    #       .until(lambda x: not isinstance(x, functools.partial))
    #       .last()
    #     )
    #     converted = convert_to_queryable(callable)
    else:
        return None


# def get_wrapper_queryable_from_partial(callable):
#     if issubclass(callable, Iterator):
#     elif issubclass(callable, Iterable):
#         elif inspect.isgeneratorfunction(v):


class Linq(GenericModel, Iterable[T]):
# Iterable[T]を利用したいが、利用するとiteratorに変換されてしまう。https://github.com/samuelcolvin/pydantic/issues/1995
    __root__: Any = None

    def __init__(self, iterable: Union[Iterable[T], Callable[[], Iterable[T]]]):
        converted = convert_to_queryable(iterable)
        if converted is None:
            raise ValueError(f'Not queryable: {type(iterable)} {iterable}')
        super().__init__(__root__=converted)

    def __iter__(self):
        return iter(self.__root__)

    # dont implement.
    # def __len__(self):
        # 詳細は　test_python_spec_len　を参照

    def __call__(self, iterable: Iterable[T]) -> 'Linq[T]':
        """クエリをイテレータにアタッチし、新しいLinqオブジェクトを作成する。"""
        chains = self._get_chains()

        if not chains[0]._is_dummy():
            raise Exception("ルートはdummyでなければいけません。")

        del chains[0]
        latest = Linq(iterable)

        for chain in chains:
            query = chain.__root__
            func = query.func
            args = query.copy_args(latest)
            new_query = Linq(functools.partial(func, *args))
            latest = Linq(new_query)

        return latest

    def _get_root_type(self):
        # not root
        if isinstance(self.__root__, Linq):
            return -1

        if self.__root__:
            return 1  # iterable root
        else:
            return 0  # empty root

    def _is_dummy(self):
        result = self._get_root_type()
        if result == 0:
            return True
        else:
            return False

    def _is_root(self):
        result = self._get_root_type()
        if result == -1:
            return False
        else:
            return True

    def _get_query(self):
        iter = self.__root__
        if hasattr(iter, "self_index"):
            self_index = iter.self_index
            return iter

        else:
            return None

    def _get_chains(self):
        chaines = [self]
        is_root = self._is_root()

        while not is_root:
            chain: Any = self.__root__
            chaines.append(chain)
            is_root = chain._is_root()

        chaines = list(reversed(chaines))
        return chaines

    @linq
    def _items(self) -> 'Linq':
        def evalute(iterator):
            yield from iterator.__root__.items()
        partial = functools.partial(evalute, self)
        return Query(partial, 0)

    def filter(self, *funcs: Iterable[Callable[[T], bool]]) -> 'Linq[T]':
        return self.filter_and(*funcs)

    @linq
    def filter_and(self, *funcs: Iterable[Callable[[T], bool]]) -> 'Linq[T]':
        def is_all_true(target):
            for func in funcs:
                if not func(target):
                    return False
            return True

        def evalute(iterator):
            for item in iterator:
                if is_all_true(item):
                    yield item

        partial = functools.partial(evalute, self)
        return Query(partial, 1)

    # 複数のpredicateを渡せるようにする
    @linq
    def filter_or(self, *funcs: Iterable[Callable[[T], bool]]) -> 'Linq[T]':
        def is_hit(target):
            for func in funcs:
                if func(target):
                    return True
            return False

        def evalute(iterator):
            for item in iterator:
                if is_hit(item):
                    yield item

        partial = functools.partial(evalute, self)
        return Query(partial, 1)

    @linq
    def filter_not(self, *funcs: Callable[[T], bool]) -> 'Linq[T]':
        # partial = functools.partial(itertools.filterfalse, func, self)
        # return Query(partial, 1)
        raise NotImplementedError()

    @linq
    def filter_in(self, selector, *arr):
        def evalute(iterator):
            for item in iterator:
                if item in arr:
                    yield item
        partial = functools.partial(evalute, self)
        return Query(partial, 0)

    @linq
    def filter_not_in(self, arr, selector):
        def evalute(iterator):
            for item in iterator:
                if not item in arr:
                    yield item

        partial = functools.partial(evalute, self)
        return Query(partial, 0)

    @linq
    def filter_between(self, arr):
        raise NotImplementedError()

    @linq
    def filter_not_between(self, arr):
        raise NotImplementedError()

    @linq
    def filter_with_enumerate(self, func: Callable[[int, T], bool]) -> 'Linq[T]':
        def evaluate(iter):
            for index, item in enumerate(iter):
                if func(index, item):
                    yield item
        partial = functools.partial(evaluate, self)
        return Query(partial, 0)

    @linq
    def filter_with_enumerate_not(self, func: Callable[[int, T], bool]) -> 'Linq[T]':
        def evaluate(iter):
            for index, item in enumerate(iter):
                if not func(index, item):
                    yield item
        partial = functools.partial(evaluate, self)
        return Query(partial, 0)

    def filter_type(self, type_) -> 'Linq':
        type_ = None.__class__ if type_ is None else type_
        return self.filter(lambda x: isinstance(x, type_))

    def filter_type_not(self, type_):
        type_ = None.__class__ if type_ is None else type_
        return self.filter_not(lambda x: isinstance(x, type_))

    def filter_even(self) -> 'Linq':
        return self.filter(lambda x: x % 2 == 0)

    def filter_odd(self) -> 'Linq':
        return self.filter(lambda x: x % 2 != 0)

    @linq
    def distinct(self, raise_error=False) -> 'Linq':
        def evaluate_raise_true(iterator):
            dic = {}
            for item in iterator:
                if item in dic:
                    raise KeyError(f"key {item} is duplicate.")
                dic[item] = item
                yield item

        def evaluate_raise_false(iterator):
            dic = {}
            for item in iterator:
                if item in dic:
                    continue
                dic[item] = item
                yield item

        evaluate = evaluate_raise_true if raise_error else evaluate_raise_false
        partial = functools.partial(evaluate, self)
        return Query(partial)

    @linq
    def take(self, count) -> 'Linq':
        def evaluate(iterator):
            counter = 0
            for index, item in enumerate(iterator):
                if counter < count:
                    yield item
                else:
                    break
                counter += 1

        partial = functools.partial(evaluate, self)
        return Query(partial, 0)

    @linq
    def skip(self, count) -> 'Linq':
        def evaluate(iterator):
            counter = 0
            it = iterator.__iter__()

            try:
                while counter < count:
                    next(it)
                    counter += 1

                while True:
                    yield next(it)

            except StopIteration as e:
                pass

            except Exception as e:
                raise

        partial = functools.partial(evaluate, self)
        return Query(partial, 0)

    @linq
    def buffer(self, size: int) -> 'Linq':
        """返す最大の配列数を制限する　リスト化した後に取ればいいからいらないかも"""
        raise NotImplementedError()

    @linq
    def take_while(self, func) -> 'Linq':
        partial = functools.partial(itertools.takewhile, func, self)
        return Query(partial, 1)

    @linq
    def drop_while(self, func) -> 'Linq':
        partial = functools.partial(itertools.dropwhile, func, self)
        return Query(partial, 1)

    @linq
    def step(self, step: int = 1) -> 'Linq':
        if step <= 0:
            raise Exception("stepは1以上を指定してください。")

        def evaluate(iter):
            count = step
            for item in iter:
                if count % step == 0:
                    yield item
                count += 1

        partial = functools.partial(evaluate, self)
        return Query(partial, 0)

    def split(self):
        # Linq([1, 2, 3, 4, 5, 6]).split(2).dispatch(bulkinsert)
        # [[1, 2], [3, 4], [5, 6]]

        raise NotImplementedError()

    @linq
    def slice(self, start: int = 0, stop: int = None, step: int = 1) -> 'Linq':
        partial = functools.partial(itertools.islice, self, start, stop, step)
        return Query(partial, 0)

    @linq
    def map(self, func: Callable[[T], R]) -> 'Linq[R]':
        partial = functools.partial(map, func, self)
        return Query(partial, 1)

    @linq
    def select(self, func: Callable[[T], R]) -> 'Linq[R]':
        partial = functools.partial(map, func, self)
        return Query(partial, 1)

    @linq
    def map_enumerate(self, func: Callable[[int, T], R]) -> 'Linq[R]':
        raise NotImplementedError()
    
    def parse(self, type_: Type[T], type_name: Optional[NameFactory] = None) -> 'Linq[R]':
        """要素を指定した型に解釈します。解釈は、pydanticのparse_obj_asを利用します。"""
        mapper = lambda x: parse_obj_as(type_, x, type_name=type_name)
        return self.map(mapper)

    def regex(self):
        raise NotImplementedError()
    
    def flatten(self) -> 'Linq':
        raise NotImplementedError()

    def fill(self, default = 0) -> 'Linq[T]':
        return self.map(lambda x: default if x is None else x)

    def zip(self, *iterable) -> 'Linq':
        return self.zip_shortest(*iterable)

    def pivot(self, default=None):
        raise NotImplementedError()

    @linq
    def zip_shortest(self, *iterable) -> 'Linq':
        def evaluate(iter, self):
            iter.insert(0, self)
            return zip(*iter)
        partial = functools.partial(evaluate, iterable, self)
        return Query(partial, 1)

    @linq
    def zip_longest(self, *iterable, fillvalue=None) -> 'Linq':
        def evaluate(iter, self):
            iter.insert(0, self)
            return itertools.zip_longest(*iter, fillvalue=fillvalue)
        partial = functools.partial(evaluate, iterable, self)
        return Query(partial, 1)

    @linq
    def cast(self, type_) -> 'Linq':
        raise NotImplementedError()

    @linq
    def select_many(self, selector=lambda x: x) -> 'Linq':
        def evaluate(iter):
            arr = map(selector, iter)
            return itertools.chain.from_iterable(arr)
        partial = functools.partial(evaluate, self)
        return Query(partial, 0)

    def select_recursive(self, selector=lambda x: x.nodes):
        
        def recursive(iterator):
            for item in iterator:
                yield item
                next_iterator = selector(item)
                yield from recursive(next_iterator)

        partial = functools.partial(recursive, self)
        return Query(partial, 0)

    def expand(self, expander=lambda x: [x]):
        """要素からイテレータを生成する関数を引数とし、そのイテレータの要素を展開する。"""
        def evalute(iterator):
            for item in iterator:
                for item2 in expander(item):
                    yield item2
        partial = functools.partial(evalute, self)
        return Query(partial, 0)

    @linq
    def lookup(self, key_selector):
        """指定されたキー セレクター関数および要素セレクター関数に従って、Lookup<TKey,TElement> から IEnumerable<T> を作成します。"""
        # var result = dictionary.ToLookup(item => item.Value[0], item => item.Key);
        raise NotImplementedError()

    @linq
    def group_by(self, func):
        raise NotImplementedError()

    @linq
    def hook(self, func=lambda index, obj: print("{}: {}".format(index, obj))):
        """デバッグ等の目的のために、処理を注入します。map関数ではないため、返されたオブジェクトは無視されます。"""
        def evalute(iterator):
            for index, item in enumerate(iterator):
                func(index, item)
                yield item
        partial = functools.partial(evalute, self)
        return Query(partial, 0)

    def hook_if(
        self,
        predicate,
        func=lambda func_name, index, obj: print(f"{func_name} {index}: {obj}")
    ) -> 'Linq[T]':
        def evalute(iterator):
            for index, item in enumerate(iterator):
                if predicate(index, item):
                    func(predicate.__name__, index, item)
                yield item
        partial = functools.partial(evalute, self)
        return Query(partial, 0)


    def raise_if(self, predicate, exc=lambda func_name, index, obj: ValueError(f"{func_name} {index}: {obj}")) -> 'Linq[T]':
        def evalute(iterator):
            for index, item in enumerate(iterator):
                if predicate(index, item):
                    raise exc(predicate.__name__, index, item)
                yield item
        partial = functools.partial(evalute, self)
        return Query(partial, 0)

    def raise_if_none(self, exc=lambda func_name, index, obj: ValueError(f"{func_name} {index}: {obj}")) -> 'Linq[T]':
        def deny_none(x):
            return x is None
        return self.raise_if(predicate=deny_none, exc=exc)

    @linq
    def default_if_empty(self):
        raise NotImplementedError()

    @linq
    def repeat(self, count):
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
        partial = functools.partial(reversed, self)
        return Query(partial, 0)

    @linq
    def shuffle(self) -> 'Linq':
        raise NotImplementedError()

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
        # return self.__root__.__getitem__(index)
        raise NotImplementedError()

    def element_at_or_default(self):
        raise NotImplementedError()

    def _one_or_undefined(self):
        result = undefined
        for index, item in enumerate(self):
            if index == 0:
                result = item
            if index > 0:
                raise LookupError("element not one.")

        return result

    def one_or_none(self):
        return self.one_or_default(None)

    def one(self) -> T:
        result = self._one_or_undefined()
        if isinstance(result, Undefined):
            raise IndexError("element not exists.")

        return result

    def one_or_default(self, default=None):
        result = self._one_or_undefined()
        if isinstance(result, Undefined):
            result = default

        return result

    def _first_or_undefined(self):
        result = undefined
        for index, item in enumerate(self):
            if index == 0:
                result = item
            break

        return result

    def first_or_none(self):
        return self.first_or_default(None)

    def first(self):
        result = self._first_or_undefined()
        if isinstance(result, Undefined):
            raise IndexError("element not exists.")

        return result

    def first_or_default(self, default=None):
        result = self._first_or_undefined()
        if isinstance(result, Undefined):
            result = default

        return result

    def _last_or_undefined(self):
        result = undefined
        for item in self:
            result = item

        return result

    def last_or_none(self):
        return self.last_or_default(None)

    def last(self):
        result = self._last_or_undefined()
        if isinstance(result, Undefined):
            raise IndexError("element not exists.")

        return result

    def last_or_default(self, default=None):
        result = self._last_or_undefined()
        if isinstance(result, Undefined):
            result = default

        return result

    # 判定
    def contains(self) -> bool:
        raise NotImplementedError()

    def all(self) -> bool:
        return all(self)

    def any(self) -> bool:
        return any(self)

    def sequence_equal(self):
        raise NotImplementedError()

    def len(self) -> int:
        count = 0
        for item in self:
            count += 1

        return count

    @linq
    def compare(self, comparison_iterator, fillvalue=undefined) -> 'Linq[bool]':
        def evaluate(iterator):
            query = Linq(comparison_iterator)
            yield from [a == b and type(a) is type(b) for a, b in itertools.zip_longest(iterator, query, fillvalue=undefined)]
        partial = functools.partial(evaluate, self)
        return Query(partial, 0)

    # 統計
    def count(self, selector: Callable[[T], R] = None) -> int:
        if selector:
            return self.map(selector).count()
        else:
            return self.len()

    def max(self, selector: Callable[[T], R] = None) -> float:
        if selector:
            return self.map(selector).max()
        else:
            return max(self)

    def min(self, selector: Callable[[T], R] = None) -> float:
        if selector:
            return self.map(selector).min()
        else:
            return min(self)

    def sum(self, selector: Callable[[T], R] = None) -> float:
        if selector:
            return self.map(selector).sum()
        else:
            return sum(self)

    def average(self, selector: Callable[[T], R] = None) -> float:
        if selector:
            return self.map(selector).average()
        else:
            # return numpy.mean(self) # -> ひとつの平均しか出さない
            return pd.Series(self).rolling(5, min_periods=1).mean()

    def median(self):
        pass

    def mode(self):
        pass

    def aggregate(self):
        raise NotImplementedError()

    def reduce(self):
        # functools.reduce
        raise NotImplementedError()

    @linq
    def accumulate(self, selector: Callable[[T], float] = lambda x: x, expression: Callable[[float, float], float] = operator.add) -> 'Linq[float]':
        query = self.map(selector)
        partial = functools.partial(itertools.accumulate, query, expression)
        return Query(partial)

    # 処理実行
    def dispatch(self, *args: Iterable[Callable[[Any], Any]]) -> NoReturn:
        """ファンクションに要素を送出します。ファンクションはいくつも渡すことができます。"""

        for item in self:
            for func in args:
                func(item)

    # 処理実行
    def each(self, *args: Iterable[Callable[[Any], Any]]) -> NoReturn:
        """ファンクションに要素を送出します。ファンクションはいくつも渡すことができます。"""

        for item in self:
            for func in args:
                func(item)

    def lazy(self):
        pass
        #
        # Linq([1,2,3,4,5,6]).split(3).dispatch(bulkinsert)
        # ↓
        # Linq([1,2,3,4,5,6]).split(3).lazy().dispatch(bulkinsert).do()
        # task = Linq.dummy().split(3).dispatch(bulkinsert)  # dummyはlazy状態になる
        # task.do([1,2,3,4,5,6]) # dummyはlazy状態になる

    # finalizer
    def to_list(self) -> List[T]:
        return list(self)

    def to_tupple(self):
        raise NotImplementedError()

    def to_dict(self):
        # def dict_override_true():
        #     dic = {}
        #     for item in self:
        #         key = key_selector(item)
        #         dic[key] = item
        #
        # def dict_override_false():
        #     dic = {}
        #     for item in self:
        #         key = key_selector(item)
        #         if key in dic:
        #             raise KeyError(f"dupulicate key:{key}")
        #         dic[key] = item
        #
        # factory = dict_override_true if override else dict_override_false
        return dict(self)

    def to_numpy(self):
        raise NotImplementedError()

    def to_dataframe(self):
        # 要は２次元配列をdataframeと呼ぶ
        # pd.DataFrame([[1,2,3],[4,5,6]])
        # col_1 col_2 col_3
        # 1     2     3
        # 4     5     6

        #  pd.DataFrame.from_dict(d, orient='index').T
        raise NotImplementedError()

    def to_series(self) -> pd.Series:
        return pd.Series(self)

    def to_parse_obj_as(self, type_: Type[R], type_name: Optional[NameFactory] = None) -> R:
        """イテレータ全体を指定した型に解釈します。解釈は、pydanticのparse_obj_asを利用します。"""
        return parse_obj_as(type_, self, type_name=type_name)

    def save(self, factory=list) -> 'Linq':
        """クエリ実行結果をルートイテレータとする新たなインスタンスを作成します。"""
        obj = self.__class__(factory(self))
        return obj

    def attach(self, iterable: Iterable[T]) -> 'Linq[T]':
        return self.__call__(iterable)

    def wrap_send_to(self, func):
        @functools.wraps(func)
        def decorated():
            return func(self())
        return decorated

    def wrap_receive_from(self, func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            result = func(*args, **kwargs)
            return self(result)
        return decorated

    @classmethod
    def flush_debug_info(cls):
        """イテレートを最新X件保持する。エラー時などに利用する。"""
        pass

    @classmethod
    def dummy(cls, iter_type: type = to_list) -> 'Linq':
        """ルートイテレータを含まないダミーオブジェクトを作成します。"""
        obj = cls([])
        obj.__root__ = None
        return obj

    @classmethod
    def graph(cls):
        from graphlib import TopologicalSorter
        return TopologicalSorter

    @classmethod
    def range(cls, stop: int, start: int = 0, step: int = 1) -> 'Linq':
        return cls(range(start=start, stop=stop, step=step))

    @classmethod
    def infinite(cls, func: Callable = lambda: 0) -> 'Linq':
        # generatorがきたらどう処理すべきか？
        def create_iterator():
            while True:
                yield func()
        return cls(create_iterator())

    @classmethod
    def from_text(cls):
        raise NotImplementedError()

    @classmethod
    def from_text_line(cls):
        raise NotImplementedError()

    @classmethod
    def from_html(cls):
        raise NotImplementedError()

    @classmethod
    def from_json(cls):
        raise NotImplementedError()

    @classmethod
    def from_csv(cls):
        raise NotImplementedError()

    @classmethod
    def from_yml(cls):
        raise NotImplementedError()

    @classmethod
    def from_xml(cls):
        raise NotImplementedError()

    @classmethod
    def from_toml(cls):
        raise NotImplementedError()

    @classmethod
    def from_excel(cls):
        raise NotImplementedError()

    @classmethod
    def from_glob(cls):
        raise NotImplementedError()






#
# class LinqDict(Linq):
#     def __init__(self, dic: Dict[T]):
#         self.__root__ = dic
#
#     def __iter__(self):
#         return self.__root__.items()


#
# # やりたいこと
# def async_func():
#     import random
#     return random.randint()
#
# cancel = False
#
# # 最大20回繰り返し、最大10個を返す
# Linq.asyncloop(
#     interval=1,
#     on_success=lambda: print("success"),
#     on_error=lambda: print("error"),
#     on_cancel=lambda: print("cancel"),
#     on_complete=lambda: print("complete")
# ).cancel(lambda: cancel == False).buffer(10).take(20).infinite(async_func).dispatch(print)

class Observer(BaseModel):
    action: Callable

    def on_next(self, value):
        self.action(value)

class Observable:
    subscribe :Callable[[Observer], Any]

    def subscribe(self, observer: Observer):
        self.subscribe(observer)


# post 属性を作成する　すでに属性が存在している場合失敗
# put 属性を作成する or 属性を置き換える　依存性による失敗はしない
# patch 属性を更新する　属性が存在しない場合は失敗
# drop 属性を削除する　属性が存在しない場合は失敗
# undefined 属性を削除する　依存性による失敗はしない


class Field(BaseModel):
    name: str

    def __call__(self, x):
        return getattr(x, self.name)

    def __eq__(self, value):
        return lambda x: getattr(x, self.name) == value

    def __ne__(self, value):
        return lambda x: not getattr(x, self.name) == value


class Operator(BaseModel):
    def __getattr__(self, name):
        return Field(name=name)


class LinqEvent:
    def __init__(self, on_success=None, on_error=None, on_complete=lambda: print("complete")):
        self.observers = []
        self.on_success = lambda: None if on_success is None else on_success
        self.on_error = lambda: None if on_error is None else on_error
        self.on_complete = on_complete
        self.query == Linq.dummy()

    def add_handler(self, observer):
        self.observers.append(observer)

    def occur(self, msg):
        for observer in self.observers:
            for item in observer(msg):
                pass

    def __call__(self, iterable):
        query = self.query(iterable)
        try:
            for msg in query:
                self.occur(msg)
            self.on_success()
        except Exception as e:
            self.on_error(e)
        finally:
            self.on_complete()

    def stream(self, iterable):
        self.__call__(iterable)

