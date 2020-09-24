import asyncio
import json
import logging
from enum import Enum
from inspect import signature
from pydantic import BaseModel
from rabbitmq.schemas import FunctionWrapper, Message

import pika
#TODO: encoderを差し替えられるようにする
from fastapi.encoders import jsonable_encoder

# infoだとログの量が多いため出力を抑制する
logging.getLogger("pika").setLevel(logging.WARNING)
logging.getLogger("pika").propagate = False


class DelayTask:
    def __init__(self, func, broker_url, queue_name):
        self.broker_url = broker_url
        self.queue_name = queue_name

        self.func_wrapper = FunctionWrapper(
            func_name=func.__name__,
            func=func
        )

    @property
    def _func(self):
        return self.func_wrapper.func

    @property
    def func_name(self):
        return self.func_wrapper.name

    @property
    def func_type(self):
        return self.func_wrapper.func_type

    def enumrate_arg_converter(self, func):
        sig = signature(func)
        for k, t in sig.parameters.items():
            if issubclass(t.annotation, BaseModel):
                yield k, lambda x: t.annotation(**x)
            else:
                pass


    def get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(self.broker_url))

    def delay(self, *args, **kwargs):
        connection = self.get_connection()
        channel = connection.channel()

        body = self.func_wrapper.encode_arg_to_json(args=args, kwargs=kwargs)
        result = channel.basic_publish(exchange="", routing_key=self.queue_name, body=body)

        connection.close()


    def consume(self, msg: Message):
        args = []
        arg = self.func_wrapper.decode_json_arg(*args, **msg.kwargs)
        return self(*args, **arg)


    def __call__(self, *args, **kwargs):
        return self.func_wrapper(*args, **kwargs)
