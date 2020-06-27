import logging
import json
import pika
import asyncio
from enum import Enum

# infoだとログの量が多いため出力を抑制する
logging.getLogger("pika").setLevel(logging.WARNING)
logging.getLogger("pika").propagate = False

class DelayTask:
    class FuncType(int, Enum):
        NORMAL = 0
        ASYNC = 1

    def __init__(self, func, broker_url, queue_name):
        self._func = func
        self.func_name = func.__name__
        self.broker_url = broker_url
        self.queue_name = queue_name

        if asyncio.iscoroutinefunction(func):
            self.func_type = self.FuncType.ASYNC
        else:
            self.func_type = self.FuncType.NORMAL


    def get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(self.broker_url))

    def delay(self, *args, **kwargs):
        connection = self.get_connection()
        channel = connection.channel()

        message = dict(
            func=self.func_name,
            args=args,
            kwargs=kwargs
        )

        if len(args) == 0:
            del message["args"]

        if len(kwargs) == 0:
            del message["kwargs"]

        body = json.dumps(message, ensure_ascii=False)

        channel.basic_publish(exchange="",
                              routing_key=self.queue_name,
                              body=body)

        connection.close()


    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)
