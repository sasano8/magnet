import typer
import click
import os

app = typer.Typer(help="Manage asgi server.")

@app.command()
def start():
    """Enumrate key-value with dockerfm.toml."""
    os.environ['IS_SELENIUM_DEBUG'] = 'True'
    # start_server(True)


def debug_start():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
