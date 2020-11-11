import pytest
from . import override_get_db


def compare(actual, expected: dict):
    for key in expected.keys():
        assert getattr(actual, key) == expected[key]
    return True


def test_get_db_unique_session():
    """get_dbはグローバルセッションを使いまわししているのでなく、独立したセッションを生成していることを確認する"""
    session1 = None
    session2 = None

    for db1 in override_get_db():
        for db2 in override_get_db():
            session1 = db1
            session2 = db2

    assert id(session1) != id(session2)


@pytest.mark.asyncio
async def test_get_db_transaction():
    """
    非同期処理により、セッションが２つ以上存在した状態でDB操作を行う可能性がある。
    それらのセッションが互いに影響を与えない、独立したセッションであることを確認する。
    """
    from magnet.scaffold import views, schemas
    for db in override_get_db():
        view = views.Dummy(db=db)
        expected = schemas.Dummy(id=1, name="created")

        actual = await view.create(expected.copy(exclude={"id"}))
        assert compare(actual, expected.dict())

        actual = await view.get(expected.id)
        assert compare(actual, expected.dict())

        expected.name = "updated"
        actual = await view.patch(id=expected.id, data=expected)
        assert compare(actual, expected.dict())

        actual = await view.copy(id=expected.id)
        dic = expected.dict()
        dic["id"] = 2
        assert compare(actual, dic)

        actual = await view.delete(id=2)
        assert actual == 1

        actual = await view.index()
        assert len(actual) == 1
        assert compare(actual[0], expected)

