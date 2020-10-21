from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from libs.fastapi import import_modules
from libs.linq import Linq
from libs.fastapi import GenericRepository, TemplateView
from magnet.env import Env
from magnet.config import logger
from magnet.database import Base, get_db, SQLALCHEMY_DATABASE_URL
from magnet.commons import BaseModel, CommonQuery, default_query

app = FastAPI()
depends_db = Depends(get_db)
rabbitmq = Env.queues["default"]


# initialize
import_modules(__file__, ["models.py"])
# import_modules(__file__, ["schemas.py"])
# import_modules(__file__, ["crud.py"])
# import_modules(__file__, ["service.py"])  # viewsはserviceに統合する
# import_modules(__file__, ["views.py"])
# import_modules(__file__, ["worker.py"])  # workerを登録しないとrabbitmqのjobが失敗する
import_modules(__file__, ["events.py"])  # fastapiにイベントを登録する


