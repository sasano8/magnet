import typer
import click
import os
import asyncio

app = typer.Typer(help="Manage elasticsearch.")


@app.command()
def start(app: str, reload:bool = False, debug: bool = False):
    """Enumrate key-value with dockerfm.toml."""
    pass
