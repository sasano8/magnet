from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Query,
                     Security, status)
from enum import Enum
from typing import List
from sqlalchemy.orm import Session
from magnet.database import get_db, TrapDB, TemplateView
from . import models, crud, schemas


class ResearchMenu(str, Enum):
    default = "default"
    carefully = "carefully"
    stock = "stock"

class Language(str, Enum):
    jp = "jp"
    en = "en"

router = APIRouter()
v_casenode = TemplateView(rep=crud.Casenode)
v_target = TemplateView(rep=crud.Target)


@router.get("/case", response_model=List[schemas.CaseNodeBase])
async def list_casenode(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return v_casenode.list(
        db=db, skip=skip, limit=limit
    )


@router.get("/case/{id}", response_model=schemas.CaseNodeBase)
async def get_casenode(id: int, db: Session = Depends(get_db)):
    return v_casenode.get(db, id=id)


@router.post("/case", response_model=schemas.CaseNodeBase)
async def create_casenode(input: schemas.CaseNodeCreate, db: Session = Depends(get_db)):
    with TrapDB():
        result = crud.Casenode.create(db, input=input)

    return result

@router.delete("/case/{id}", status_code=200)
async def delete_casenode(id: int, db: Session = Depends(get_db)):
    with TrapDB():
        crud.Casenode.delete(db, id=id)


@router.patch("/case/{id}", response_model=schemas.CaseNodeUpdate)
async def update_casenode(id: int, input: schemas.CaseNodeUpdate, ignore_unknown_attr: bool = False, db: Session = Depends(get_db)):
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

    with TrapDB():
        result = crud.Casenode.update(db, input)

    return result



@router.post("/case/{src_id}", response_model=schemas.CaseNodeUpdate)
async def copy_casenode(src_id: int, override: schemas.CaseNodeUpdate, dest_id: int = None, ignore_unknown_attr: bool = False, db: Session = Depends(get_db)):
    if ignore_unknown_attr:
        pass
        # TODO: タイポなど誤った属性入力時にエラーとする

    if hasattr(override, "id"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can not allow to override id.".format(id, override.id))

    with TrapDB():
        result = crud.Casenode.duplicate(db, src_id=src_id, overrides=override.to_dict(), dest_id=dest_id)

    return result




@router.get("/target", response_model=List[schemas.TargetBase])
async def list_target(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    with TrapDB():
        results = crud.Target.list(
            db=db, skip=skip, limit=limit
        )

    return results


@router.get("/target/{id}", response_model=schemas.TargetBase)
async def get_target(id: int, db: Session = Depends(get_db)):
    with TrapDB():
        result = crud.Target.get(db, id=id)

    return result


@router.post("/target", response_model=schemas.TargetBase)
async def create_target(input: schemas.TargetCreate, db: Session = Depends(get_db)):
    with TrapDB():
        result = crud.Target.create(db, input=input)

    return result

@router.delete("/target/{id}", status_code=200)
async def delete_target(id: int, db: Session = Depends(get_db)):
    with TrapDB():
        crud.Target.delete(db, id=id)


