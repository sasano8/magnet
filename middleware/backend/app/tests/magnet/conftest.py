from magnet import Base, get_db
from pytest import fixture
import main
from magnet import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@fixture(autouse=True, scope="session")
def override_dependency():
    """
    テスト用データベースに切り替える。
    REST API経由のテスト実行をサポートするため、テスト完了時に依存データベースを元に戻す
    """

    # setup
    print("setup!!!!")
    main.app.dependency_overrides[get_db] = override_get_db
    yield
    # shutdown
    print("shutdown!!!")
    main.app.dependency_overrides[get_db] = get_db
