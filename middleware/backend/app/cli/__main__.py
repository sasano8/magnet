import os
import typer
import click

from cli import cli_rabbitmq
from cli import cli_uvicorn
from cli import cli_elasticsearch
from cli import cli_dev

app = typer.Typer()
app.add_typer(cli_rabbitmq.app, name="worker")
app.add_typer(cli_uvicorn.app, name="uvicorn")
app.add_typer(cli_elasticsearch.app, name="elasticsearch")
app.add_typer(cli_dev.app, name="dev")


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