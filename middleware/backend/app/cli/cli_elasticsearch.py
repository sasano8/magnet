import asyncio
import os

import click
import typer

app = typer.Typer(help="Manage elasticsearch.")


@app.command()
def start(app: str, reload: bool = False, debug: bool = False):
    """Enumrate key-value with dockerfm.toml."""
    pass
