import os
import typer
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
    # from magnet import config
    # from magnet.database import SQLALCHEMY_DATABASE_URL
    from magnet import SQLALCHEMY_DATABASE_URL
    from sqlalchemy_utils import create_database, database_exists
    if not database_exists(str(SQLALCHEMY_DATABASE_URL)):
        logger.warning("[START]create database.")
        create_database(str(SQLALCHEMY_DATABASE_URL))
    else:
        logger.warning("[SKIP]create database.")


@app.command()
def drop():
    from sqlalchemy_utils import drop_database
    # from magnet import config
    from magnet import SQLALCHEMY_DATABASE_URL
    drop_database(str(SQLALCHEMY_DATABASE_URL))


@app.command()
def makemigrations():
    import datetime
    alembic_cfg = get_alembic_cfg()
    rev_id = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    alembic_command.revision(alembic_cfg, head="head", autogenerate=True, rev_id=rev_id)


@app.command()
def migrate():
    # データベースを事前に作成しないと、マイグレーションが適用されない
    create_database()

    alembic_cfg = get_alembic_cfg()
    alembic_command.upgrade(alembic_cfg, revision="head")


@app.command()
def output_design():
    import eralchemy
    from magnet import Base
    eralchemy.render_er(Base, "er.png")
    markdown = get_table_define_as_markdown(Base)
    with open("tables.md", mode='w') as f:
        f.write(markdown)


def dump():
    pass


def load():
    pass


def get_table_define_as_markdown(base):
    tables = [x for x in base.metadata.tables.values()]
    arr = []

    for table in tables:
        """
        'key', 
        'name',
        'table',
        'type',
        'is_literal',
        'primary_key',
        'nullable',
        'default',
        'server_default',
        'server_onupdate',
        'index',
        'unique',
        'system',
        'doc',
        'onupdate',
        'autoincrement',
        'constraints',
        'foreign_keys',
        'comment',
        'computed',
        '_creation_order',
        'dispatch',
        'proxy_set',
        'description',
        'comparator',
        '_cloned_set',
        '_from_objects',
        '_label',
        '_key_label',
        '_render_label_in_columns_clause'
        """

        arr.append("## " + table.name)
        if table.comment:
            arr.append(table.comment)
            arr.append("")
        arr.append("| name | type | pk | unique | index | nullable | default | comment |")
        arr.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
        for column in table._columns.values():

            dic = create_column_info_as_dict(
                name=column.name,
                type_=column.type,
                pk=column.primary_key,
                unique=column.unique,
                index=column.index,
                nullable=column.nullable,
                default=column.default,
                comment=column.comment,
            )

            s = "| {name} | {type} | {pk} | {unique} | {index} | {nullable} | {default} | {comment} |".format(**dic)
            arr.append(s)

        arr.append("")

    return "\n".join(arr)


def create_column_info_as_dict(name, type_, pk, unique, index, nullable, default, comment):
    def get_value_or_empty(value):
        if value is None:
            return ""
        else:
            return value

    def get_str_or_ohter(value):
        if isinstance(value, str) and value == "":
            return "\"\""

        return value

    try:
        type_ = str(type_)
    except:
        # JSONカラムの場合、なぜか文字列化できない。それ以外のカラムで、発生するかは知らん。
        type_ = type(type_).__name__

    # 設計書にNoneが表示されるのが煩わしいため空文字にする
    return dict(
        name=get_value_or_empty(name),
        type=get_value_or_empty(type_),
        pk="x" if pk else "",
        unique="x" if unique else "",
        index="x" if index else "",
        nullable="x" if nullable else "",
        default=get_str_or_ohter(default.arg) if default else "",
        comment=get_value_or_empty(comment),
    )
