from libs.inspect import ObjectInfo


def func():
    pass


class Dummy:
    def method(self):
        pass


def test_object_info():
    info = ObjectInfo(func)
    assert info.is_function
    assert not info.is_method
    assert not info.is_unbounded_method
    assert not info.is_static_method

    info = ObjectInfo(Dummy.method)
    assert info.is_function
    assert not info.is_method  # インスタンスが作成されるまではmethodではない
    assert info.is_unbounded_method
    assert not info.is_static_method

    info = ObjectInfo(Dummy().method)
    assert not info.is_function
    assert info.is_method
    assert not info.is_unbounded_method
    assert not info.is_static_method

