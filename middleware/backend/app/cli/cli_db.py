import os
import typer
from magnet.database import Base, engine
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
import logging
logger = logging.getLogger("magnet")
logger.setLevel("INFO")

app = typer.Typer(help="Manage local server for development.")

def get_alembic_cfg():
    cd = os.getcwd()
    alembic_path = os.path.join(cd, "alembic.ini")
    alembic_cfg = AlembicConfig(alembic_path)
    return alembic_cfg


def create_database(delete_database: bool = False):
    from magnet import config
    from sqlalchemy_utils import create_database, database_exists
    if not database_exists(str(config.SQLALCHEMY_DATABASE_URL)):
        logger.warning("[START]create database.")
        create_database(str(config.SQLALCHEMY_DATABASE_URL))
    else:
        logger.warning("[SKIP]create database.")

@app.command()
def drop():
    from sqlalchemy_utils import drop_database
    from magnet import config
    drop_database(str(config.SQLALCHEMY_DATABASE_URL))


@app.command()
def makemigrations():
    import datetime
    from magnet import database
    logger.info("import module.")
    database.import_all_models_py()

    alembic_cfg = get_alembic_cfg()
    rev_id = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    alembic_command.revision(alembic_cfg, head="head", autogenerate=True, rev_id=rev_id)


@app.command()
def migrate():
    # データベースを事前に作成しないと、マイグレーションが適用されない
    create_database()

    alembic_cfg = get_alembic_cfg()
    alembic_command.upgrade(alembic_cfg, revision="head")


def dump():
    pass

def load():
    pass
