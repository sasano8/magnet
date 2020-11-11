from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from libs.fastapi import import_modules
from libs.linq import Linq
from libs.fastapi import GenericRepository, TemplateView
from magnet.env import Env
from magnet.config import logger
from magnet.database import Base, get_db, SQLALCHEMY_DATABASE_URL, create_test_engine
from magnet.commons import BaseModel, PagenationQuery

app = FastAPI()
depends_db = Depends(get_db)
rabbitmq = Env.queues["default"]


module_file_names = [
    "models.py",
    # "schemas.py",
    # "crud.py",  # dispatchの場合、serviceと読んでいる。
    # "views.py",
    # "worker.py",
    "events.py"
]

# initialize
for module_file_name in module_file_names:
    import_modules(__file__, [module_file_name])
