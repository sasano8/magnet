import asyncio
import random
import json
import pika

from importlib import import_module


def start_consumer(target_module):
    from watcher import FileChangeDetector

    while True:
        from importlib import import_module
        module, attr = target_module.split(":")
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




