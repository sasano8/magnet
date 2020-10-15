from magnet import rabbitmq
from magnet.crawler import service
from magnet.ingester import schemas

@rabbitmq.task
def exec_job(job: schemas.TaskCreate):
    service.exec_job(job=job)

