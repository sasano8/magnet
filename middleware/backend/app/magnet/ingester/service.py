from sqlalchemy.orm import Session
from . import schemas, crud, impl
from fastapi import HTTPException
from magnet.executor import worker

JOBGROUP_ROOT_ID = 0


def get_or_create_jobgroup_root(db: Session):
    jobgroup = crud.IngesterJobGroup.get(db=db, id=JOBGROUP_ROOT_ID)

    if jobgroup is None:
        obj = schemas.JobGroupCreate(
            id=JOBGROUP_ROOT_ID,
            description="root",
            is_system=True
        )
        jobgroup = crud.IngesterJobGroup.create(db, obj)

    return jobgroup


def create_job(db: Session, input: schemas.JobCreate):
    if input.jobgroup_id is None:
        input.jobgroup_id = JOBGROUP_ROOT_ID

    if input.jobgroup_id == JOBGROUP_ROOT_ID:
        jobgroup = get_or_create_jobgroup_root(db)
    else:
        jobgroup = crud.IngesterJobGroup.get(db, id=input.jobgroup_id)
        if jobgroup is None:
            raise HTTPException(status_code=404, detail="Not found a job group.")

    dic = input.dict(exclude={"jobgroup_id"})
    job = crud.IngesterJob.model(**dic)

    job.parent_id = jobgroup.id
    db.add(job)
    db.commit()
    db.refresh(job)
    exec_job_by_id(db, job.id)
    return job

def exec_job_by_id(db: Session, id: int):
    job = crud.IngesterJob.get(db=db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="not found id.")

    payload = schemas.CommonSchema.from_orm(job)
    payload = schemas.TaskCreate(**payload.dict())

    try:
        worker.exec_job.delay(job=payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# queue
def list(db: Session, skip: int = 0, limit: int = 100):
    return crud.Ingester.list(db, skip=skip, limit=limit)


def get(db: Session, id: int):
    return crud.Ingester.get(db, id)


def create(db: Session, input: schemas.CommonSchema):
    return crud.Ingester.create(db, input)


def update(db: Session, input: schemas.CommonSchema):
    raise NotImplementedError()


def delete(db: Session, id: int):
    return crud.Ingester.delete(db, id=id)


def digest(db: Session, id: int, delete_on_complete: bool = True):
    """指定したキューを消化する"""
    raise NotImplementedError()


def delete_all(db: Session):
    return crud.Ingester.delete_all(db)


# ingester
def get_ingester_by_name(ingester_name: str):
    if "postgres" == ingester_name:
        return impl.Postgress
    elif "elastic" == ingester_name:
        raise NotImplementedError()
    else:
        raise KeyError()
