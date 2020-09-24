import pytest
from libs.linq import Linq


def test_linq():
    linq = Linq([1,2,3,4,5,6])
    arr = linq.filter(lambda x: x % 2 == 0).list()

    print(arr)
    assert arr == [2, 4, 6]




