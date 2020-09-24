import os

import click
import typer

from cli import cli_dev, cli_elasticsearch, cli_rabbitmq, cli_uvicorn, cli_db

app = typer.Typer()
app.add_typer(cli_rabbitmq.app, name="worker")
app.add_typer(cli_uvicorn.app, name="uvicorn")
app.add_typer(cli_elasticsearch.app, name="elasticsearch")
app.add_typer(cli_dev.app, name="dev")
app.add_typer(cli_db.app, name="db")


# # resilient_parsing: dockerfm.tomlが存在する場合、対話形式のプロンプトを無視する。値はNoneとなる。
# @app.command()
# def worker(
#     user_name: str = typer.Option(prompt=True, default="yourname",),
#     project_name: str = typer.Option(prompt=True, default="sample"),
#     dockerfm_dir: str = typer.Option(prompt=True, default="./dockerfm/"),
#     create_template: bool = typer.Option(
#         prompt="Create template dockerfm directories?", default=False
#     ),
# ):
#     """Manage rabbitmq consumers."""
#     pass


if __name__ == "__main__":
    app()
