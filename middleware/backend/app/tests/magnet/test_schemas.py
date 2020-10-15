import pytest
from pydantic import BaseModel

def test_pydantic():
    class A(BaseModel):
        age: int

    try:
        obj = A(age="a")

    except Exception as e:
        obj = e
        raise
