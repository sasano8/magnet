import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query, Session
from magnet import config

logger = config.getLogger()

if config.SQLALCHEMY_DATABASE_URL.startswith('sqlite'):
    logger.warning("sqliteはalembicのauto migrationに完全対応していません。")
    kwargs = {"check_same_thread": False}
else:
    kwargs = {}


engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL, connect_args=kwargs
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def enumrate_models_py():
    """
    Enumrate models.py's path as sqlalchemy model definition.
    This operation is useful for automatically importing sqlalchemy models.
    """
    target_dir = os.path.dirname(__file__)

    for reload_dir in [target_dir]:
        for subdir, dirs, files in os.walk(reload_dir):
            for file in files:
                if file == "models.py":
                    yield subdir + os.sep + file


def convert_path_to_importable(file):
    cd = os.path.dirname(__file__)
    dir_name = os.path.basename(cd)

    tmp1 = file.replace(cd, "").lstrip("/")
    tmp2 = tmp1.replace("/", ".")
    module = dir_name + "." + tmp2[:-3]  # remove .py

    return module

def import_all_models_py():
    """models.pyを収集し、全てインポートする"""
    import importlib

    arr = list(enumrate_models_py())

    logger.info("Scanning models.py")
    for file in arr:
        module = convert_path_to_importable(file)
        logger.info(module)
        importlib.import_module(module)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.debug(f"close database connection.")





from fastapi import (HTTPException, status)
from sqlalchemy.orm import exc


class TrapDB(object):
    """sqlalchemyで発生する例外をHTTPExceptionにマップしraiseする。想定外の例外はそのままraiseされる。"""
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_value == None:
            return True

        if exc_type is exc.NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        else:
            # The exception will be rethrow if False is returned.
            return False


from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Any, ClassVar, Generic, TypeVar, Type
from sqlalchemy.orm import Session


def paginate(query: Query, page: int, items_per_page: int):
    # Never pass a negative OFFSET value to SQL.
    offset_adj = 0 if page <= 0 else page - 1
    items = query.limit(items_per_page).offset(offset_adj * items_per_page).all()
    total = query.order_by(None).count()
    return items, total


Alchemy = TypeVar('Alchemy')


class GenericRepository(GenericModel, Generic[Alchemy]):
    model: Type[Alchemy]

    @classmethod
    def get_model(cls) -> Type[Alchemy]:
        _type = cls.__fields__["model"].outer_type_
        _class = _type.__args__[0]
        return _class

    def __init__(self):
        model = self.get_model()
        super().__init__(model=model)

    def query(self, db: Session) -> Query:
        return db.query(self.model)

    def list(self, db: Session, skip: int = 0, limit: int = 100):
        return self.query(db).offset(skip).limit(limit).all()

    def get(self, db: Session, id: int) -> Alchemy:
        return self.query(db).filter(self.model.id == id).one_or_none()

    def upsert(self, db: Session, input: BaseModel) -> Alchemy:
        obj = self.update(db, input)
        if obj:
            return obj
        else:
            return self.create(db, input)

    def create(self, db: Session, input: BaseModel) -> Alchemy:
        obj = self.model(
            **input.dict()
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> int:
        count = self.query(db).filter(self.model.id == id).delete()
        db.commit()
        return count

    def delete_all(self, db: Session) -> int:
        count = self.query(db).delete()
        db.commit()
        return count

    def put(self, db: Session, input: BaseModel) -> Alchemy:
        self.query(db).filter(self.model.id == input.id).delete()
        obj = self.create(db, input)
        return obj

    def put_cascade(self, db: Session, input: BaseModel) -> Alchemy:
        # TODO: 単純なputの場合、delete時に関係データを削除してしまうため、削除せずに置き換える方法を考える
        raise NotImplementedError()

    def update(self, db: Session, input: BaseModel) -> Alchemy:
        obj = self.query(db).filter(self.model.id == input.id).one_or_none()
        if obj is None:
            return None

        dic = input.dict(exclude_unset=True)
        self.__patch_attribute__(obj, dic)
        db.commit()
        db.refresh(obj)
        return obj

    def __patch_attribute__(self, obj, kwargs):
        """kwargsに対応するobjの属性を更新する"""
        for key, value in kwargs.items():
            setattr(obj, key, value)

    def duplicate(self, db: Session, src_id: int, overrides: dict = None, dest_id: id = None) -> Alchemy:
        # TODO: dest_idが被った場合はどうなる？
        # TODO: overrides内のidとdest_idの検証
        obj = self.get(db, src_id)
        if obj is None:
            return None

        if overrides is not None:
            self.__patch_attribute__(obj, overrides)

        obj.id = dest_id
        db.add(obj)
        db.refresh(obj)
        return obj


class TemplateView(BaseModel):
    """汎用的に利用する機能をテンプレート化する。独自にAPIを実装する場合は、無理に当該クラスを継承せず、直接API実装箇所に実装してしまえばよい。"""
    rep: GenericRepository

    def list(self, db: Session, skip: int = 0, limit: int = 100):
        results = self.rep.list(
            db=db, skip=skip, limit=limit
        )
        return results

    def get(self, db: Session, id: int):
        result = self.rep.get(db, id=id)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return result

    def create(self, db: Session, input: BaseModel):
        result = self.rep.create(db, input=input)
        return result

    def delete(self, db: Session, id: int):
        result = self.rep.delete(db, id=id)

        if result == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return result


    def update(self, db: Session, input: BaseModel, ignore_unknown_attr: bool = False):
        if ignore_unknown_attr:
            pass
            # TODO: タイポなど誤った属性入力時にエラーとする

        if hasattr(input, "id"):
            if (input.id is not None) and (not id == input.id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Can not allow to update id. targeted id:{} requested id:{}.".format(id,
                                                                                                                input.id))
            else:
                if id is not None:
                    input.id = id

        result = self.rep.update(db, input)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return result

    def duplicate(self, db: Session, src_id: int, overrides: dict = None, dest_id: id = None, ignore_unknown_attr: bool = False):
        if ignore_unknown_attr:
            pass
            # TODO: タイポなど誤った属性入力時にエラーとする

        if hasattr(overrides, "id"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Can not allow to override id.".format(id, overrides.id))

        result = self.rep.duplicate(db, src_id=src_id, overrides=overrides.to_dict(), dest_id=dest_id)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return result

