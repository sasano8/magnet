import asyncio
import os
from typing import List

import click
import typer

app = typer.Typer(help="Manage rabbitmq consumers.")


@app.command()
def start(app: str, reload: bool = False, debug: bool = False):
    """Enumrate key-value with dockerfm.toml."""
    start_worker(app, reload)


def start_worker(reload: bool = False, debug: bool = False, app_names: List[str] = []):
    import sys

    app_name = app_names[0]

    from importlib import import_module

    cd = os.getcwd()
    module, attr = app_name.split(":")

    print("current :{}".format(cd))

    if module in sys.modules:
        sys.modules.pop(module)

    module = import_module(module)

    app = getattr(module, attr)

    consumer = app.get_consumer()

    loop = None
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(consumer.consume())

    except KeyboardInterrupt as e:
        print("購読を中止します")

    except asyncio.CancelledError as e:
        print("非同期処理がキャンセルされました。")

    finally:
        loop.close()
        consumer.stop()
