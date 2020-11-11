from pytest import fixture
import main
from magnet import Base, get_db, create_test_engine

is_local = True

if is_local:
    engine, override_get_db = create_test_engine()


@fixture(autouse=True, scope="session")
def override_dependency():
    """
    テスト用データベースに切り替える。
    REST API経由のテスト実行をサポートするため、テスト完了時に依存データベースを元に戻す
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        main.app.dependency_overrides[get_db] = override_get_db
        yield
    finally:
        main.app.dependency_overrides[get_db] = get_db
