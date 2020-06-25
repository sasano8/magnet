import typer
import click
import os
import asyncio

app = typer.Typer(help="Manage rabbitmq consumers.")


@app.command()
def start(app: str, reload:bool = False, debug: bool = False):
    """Enumrate key-value with dockerfm.toml."""
    start_worker(app, reload)


def start_worker(app: str, reload: bool = False, debug: bool = False):
    from watcher import FileChangeDetector

    while True:
        from importlib import import_module
        cd = os.getcwd()
        module, attr = app.split(":")

        print("current :{}".format(cd))

        module = "deco_worker"
        module = import_module(module)

        app = getattr(module, attr)

        consumer = app.get_consumer()

        loop = None
        try:
            is_changed_files = FileChangeDetector("/app")
            is_changed_files.set_callback(consumer.stop)
            watcher = is_changed_files.get_coroutine(interval=1, run_until_file_changed=True)

            loop = asyncio.new_event_loop()
            loop.create_task(consumer.run())
            result = loop.run_until_complete(watcher)

        except KeyboardInterrupt as e:
            print("購読を中止します")
            break

        finally:
            loop.close()
            consumer.stop()
