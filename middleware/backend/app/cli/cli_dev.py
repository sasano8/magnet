import typer
import click
import os
import asyncio

app = typer.Typer(help="Manage local server for development.")


@app.command()
#def start(app: str, reload:bool = False, debug: bool = False):
def start():
    """Enumrate key-value with dockerfm.toml."""
    from cli import cli_uvicorn
    from cli import cli_rabbitmq
    from multiprocessing import Process

    import time
    import asyncio
    from watcher import FileChangeDetector


    while True:
        processes = []
        asgi = Process(target=cli_uvicorn.debug_start)
        consumer = Process(target=cli_rabbitmq.start_worker, kwargs=dict(app_names=["myworker:app"]))

        processes.append(asgi)
        processes.append(consumer)

        try:
            for p in processes:
                p.start()

            time.sleep(0.5)

            loop = asyncio.new_event_loop()
            observer = FileChangeDetector("/app")
            future = observer.get_coroutine(interval=1, run_until_file_changed=True)
            result = loop.run_until_complete(future)

        finally:
            loop.stop()

            for p in processes:
                p.terminate()

            for p in processes:
                p.join()


