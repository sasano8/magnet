from enum import Enum
from typing import Generic, TypeVar, Type, Any, Tuple, Iterable, Union, List, Literal
from pydantic import BaseModel, PydanticValueError, validator, ValidationError, validate_arguments
from pydantic.generics import GenericModel
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.schema import Column
from sqlalchemy.inspection import inspect
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError


def paginate(query: Query, page: int, items_per_page: int):
    # Never pass a negative OFFSET value to SQL.
    offset_adj = 0 if page <= 0 else page - 1
    items = query.limit(items_per_page).offset(offset_adj * items_per_page).all()
    total = query.order_by(None).count()
    return items, total


Alchemy = TypeVar('Alchemy')

arr = [1, 2]


class EnumBase(Enum):
    """define enum with key-value.  EXAMPLE: FIRST = 0, 'first',"""
    def __str__(self):
        return self.msg

    @property
    def no(self):
        return self._value_[0]

    @property
    def msg(self):
        return self._value_[1]


class EMsg(EnumBase):
    E_001_NOT_PERMITTED = 1, "extra fields not permitted"
    E_002_NOT_EDIT = 2, "fields not permitted editing"


class EType(EnumBase):
    E_001_VAL_ERR_MISSING = 1, "value_error.missing"
    E_002_VAL_ERR_IMMUTABLE = 2, "value_error.immutable"


class ExcBuilder:
    def __init__(self, status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY):
        self.status_code = status_code
        self.errors = []

    def add(self,
            msg: EnumBase,
            type_: EnumBase,
            loc: tuple = ()
    ):
        self.errors.append({"loc": loc, "msg": msg.__str__(), "type": type_.__str__()})

    def build(self):
        return HTTPException(
            status_code=self.status_code,
            detail=self.errors
        )


@validate_arguments
def build_exception(
    loc: tuple,
    msg: str,
    # type_: str,
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        # detail=[{"loc": loc, "msg": msg, "type": type_}]
        detail=[{"loc": loc, "msg": msg}]
    )


class GenericRepository(Generic[Alchemy]):
    def __init__(self, db: Session = None):
        self.model: Type[Alchemy] = self.get_model()
        self.primary_keys: List[Column] = self._get_primary_keys(self.model)
        self.db = db

    @classmethod
    def get_model(cls) -> Type[Alchemy]:
        generic_type = cls.__orig_bases__[0].__args__[0]
        return generic_type

    @classmethod
    def _get_primary_keys(cls, table):
        tuple = inspect(table).primary_key
        return list(tuple)

    def contais_primary_key(self, data: BaseModel):
        for field in self.primary_keys:
            if hasattr(data, field.name):
                return True
        return False

    def query(self) -> Query:
        return self.db.query(self.model)

    def index(self, skip: int = 0, limit: int = 100) -> Union[Iterable[Alchemy], Query]:
        return self.query().offset(skip).limit(limit)

    def get(self, id: int) -> Alchemy:
        return self.query().filter(self.model.id == id).one_or_none()

    def create(self, data: BaseModel) -> Alchemy:
        if self.contais_primary_key(data):
            raise ValueError("create時にprimary keyを含めることはできません。")

        obj = self.model(
            **data.dict()
        )
        db = self.db
        db.add(obj)
        db.commit()
        db.refresh(obj)

        # トランザクション管理を極めてきたら、get_dbにauto commitを追加して、こっちにすればいいかも。
        # db.add(obj)  # 登録予約する。
        # db.flush  # SQLをデータベースに送信し、オブジェクトの状態を更新する。commit操作が最終的に必要。
        return obj

    def update(self, data: BaseModel) -> Alchemy:
        # TODO: 自動キー検出を設ける
        obj = self.query().filter(self.model.id == data.id).one_or_none()
        if obj is None:
            return None

        dic = data.dict(exclude_unset=True)  # 未設定の価は出力しない
        [setattr(obj, k, v) for k, v in dic.items()]
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def upsert(self, data: BaseModel) -> Alchemy:
        obj = self.update(data)
        if obj is None:
            obj = self.model(
                **data.dict()
            )
            db = self.db
            db.add(obj)
            db.commit()
            db.refresh(obj)

        return obj

    def delete(self, id: int) -> int:
        count = self.query().filter(self.model.id == id).delete()
        self.db.commit()
        return count

    def delete_all(self) -> int:
        count = self.query().delete()
        self.db.commit()
        return count

    def put(self, data: BaseModel) -> Alchemy:
        self.query().filter(self.model.id == data.id).delete()
        obj = self.create(data)
        return obj

    def put_cascade(self, db: Session, data: BaseModel) -> Alchemy:
        # TODO: 単純なputの場合、delete時に関係データを削除してしまうため、削除せずに置き換える方法を考える
        raise NotImplementedError()

    def duplicate(self, id: int) -> Alchemy:
        obj = self.get(id)
        if obj is None:
            return None

        obj.id = None
        self.db.add(obj)
        self.db.refresh(obj)
        return obj

    def bulk_insert(self, rows: Iterable[BaseModel], auto_commit=True) -> Tuple[int, int]:
        model = self.model
        try:
            deleted = 0
            inserted = 0

            for item in rows:
                obj = model(**item.dict())
                self.db.add(obj)
                inserted += 1

            if auto_commit:
                self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise

        return deleted, inserted

    def bulk_delete_insert(self, delete_query: Query, rows: Iterable[BaseModel], auto_commit=True) -> Tuple[int, int]:
        model = self.model

        try:
            deleted = delete_query.delete()
            inserted = 0

            for item in rows:
                obj = model(**item.dict())
                self.db.add(obj)
                inserted += 1

            if auto_commit:
                self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise

        return deleted, inserted


Repository = TypeVar("GenericRepository[Alchemy]", bound=GenericRepository[Alchemy])


class TemplateView(Generic[Repository]):
    """汎用的に利用する機能をテンプレート化する。独自にAPIを実装する場合は、無理に当該クラスを継承せず、直接API実装箇所に実装してしまえばよい。"""
    # def __init__(self):
    #     # fastapi-utils cvsが依存性定義に応じて、自動でコンストラクタを作成する。
    #     # クラス初期化時に、キーワード引数で初期化引数にアクセスすることができる。

    @property
    def db(self) -> Session:
        raise NotImplementedError()

    @classmethod
    def get_repository(cls) -> Type[Repository]:
        """継承時に指定したsqlalchemyクラスを取得します。多分、２回以上継承すると動かない。"""
        generic_type = cls.__orig_bases__[0].__args__[0]
        return generic_type

    @property
    def rep(self) -> Repository:
        repository = self.get_repository()
        return repository(self.db)

    def index(self, skip: int = 0, limit: int = 100) -> List[Alchemy]:
        results = self.rep.index(skip=skip, limit=limit)
        return list(results)

    def get(self, id: int) -> Alchemy:
        result = self.rep.get(id=id)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return result

    def create(self, data: BaseModel) -> Alchemy:
        result = self.rep.create(data=data)
        return result

    def delete(self, id: int) -> int:
        result = self.rep.delete(id=id)

        if result == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return result

    def patch(self, id: int, data: BaseModel) -> Alchemy:
        if hasattr(data, "id") and data.id != id:
            e = ExcBuilder(status.HTTP_422_UNPROCESSABLE_ENTITY)
            e.add(("id",), EMsg.E_002_NOT_EDIT, EType.E_002_VAL_ERR_IMMUTABLE)
            raise e.build()

        result = self.rep.update(data)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return result

    def duplicate(self, id: int) -> Alchemy:
        result = self.rep.duplicate(id=id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return result
