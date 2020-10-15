from magnet import BaseModel


class DispatchCreate(BaseModel):
    pipeline_name: str = "postgres"
    crawler_name: str


class ExecutorCreate(BaseModel):
    executor_name: str
    pipeline_name: str


class ExecutorBase(ExecutorCreate):
    is_system: bool = False

    class Config:
        orm_mode = True
        # extra = "ignore"



