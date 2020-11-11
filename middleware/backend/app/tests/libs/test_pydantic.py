import pytest
from pydantic import BaseModel, ValidationError
from libs.pydantic import generate_func_code, generate_funnel, funnel


def test_base_model_generate_func_code():
    class A(BaseModel):
        name: str
        age: int = 20

    code, func_name, model_name, annotations, defaults, kwdefaults = generate_func_code(A)
    # デフォルト値は暫定的にNoneと定義され、後でbindし直される
    expected = f"""def {func_name}(*,
  name,
  age=None,
):
  return {model_name}(
    name=name,
    age=age,
  )"""

    assert func_name == "tmp_func"
    assert model_name == "Model"
    assert code == expected
    assert annotations["name"] is str
    assert annotations["age"] is int
    # assert defaults
    assert "name" not in kwdefaults
    assert kwdefaults["age"] == 20


def test_generate_funnel():
    class A(BaseModel):
        name: str
        age: int = 20

    func = generate_funnel(A)

    obj = func(name="bob", age=30)
    assert obj.name == "bob"
    assert obj.age == 30

    obj = func(name="mary")
    assert obj.name == "mary"
    assert obj.age == 20

    with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'name'") as e:
        obj = func()


def test_get_queries():
    from libs.pydantic.utils import generate_fastapi_funnel, get_queries
    from pydantic import Field
    class A(BaseModel):
        name: str
        age: int = 20
        comment: str = Field(alias="description")
        class Config:
            allow_population_by_field_name = True
            fields = {
                "name": "fullname"
            }

    query = get_queries(A)
    print(query)


def test_funnel():
    class A(BaseModel):
        name: str
        age: int = 20

    @funnel
    def func(obj: A):
        return obj.dict()

    class Dummy1:
        @funnel
        def method(self, obj: A):
            return obj.dict()

        @classmethod
        @funnel
        def class_method(cls, obj: A):
            return obj.dict()

        # @funnel2
        # @classmethod
        # def class_method(cls, obj: A):
        #     return obj.dict()

        @staticmethod
        @funnel
        def static_method(obj: A):
            return obj.dict()

    test_func = func
    # function / object
    result = test_func(A(name="bob", age=30))
    assert result["name"] == "bob"
    assert result["age"] == 30

    # function / keyword
    result = test_func(name="bob2", age=31)
    assert result["name"] == "bob2"
    assert result["age"] == 31

    # function / object keyword(object has priority.)
    with pytest.raises(ValueError, match="位置限定引数とキーワード限定引数のいずれかのみ受け入れ可能です。") as e:
        result = test_func(A(name="bob", age=30), name="bob2", age=31)

    with pytest.raises(ValidationError, match="field required") as e:
        obj = func()

    obj = Dummy1()
    test_func = obj.method
    # function / object
    result = test_func(A(name="bob", age=30))
    assert result["name"] == "bob"
    assert result["age"] == 30

    # function / keyword
    result = test_func(name="bob2", age=31)
    assert result["name"] == "bob2"
    assert result["age"] == 31

    # function / object keyword(object has priority.)
    with pytest.raises(ValueError, match="位置限定引数とキーワード限定引数のいずれかのみ受け入れ可能です。") as e:
        result = test_func(A(name="bob", age=30), name="bob2", age=31)

    with pytest.raises(ValidationError, match="field required") as e:
        obj = func()

    result = obj.class_method(name="tom", age=50)
    assert result["name"] == "tom"
    assert result["age"] == 50

    result = obj.static_method(name="david", age=60)
    assert result["name"] == "david"
    assert result["age"] == 60
