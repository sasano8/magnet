import copy
import json

import pika

from rabbitmq.task import DelayTask


class Coordinator:
    def __init__(
        self,
        broker_url,
        queue_name,
        auto_ack,
        durable,
        queue_delete,
        async_concurrency=1,
    ):
        self.broker_url = broker_url
        self.queue_name = queue_name
        self.auto_ack = auto_ack
        self.durable = durable
        self.queue_delete = queue_delete

        self.tasks = {}

    def get_tasks(self):
        return copy.copy(self.tasks)

    def task(self, func_or_arg=None, *args, **kwargs):
        # TODO: タスクをdelayでなく通常呼び出しを行った場合に、位置引数を受け入れずエラーとなる　例 ex_task(param) -> NG  ex_task.delay(param) -> OK
        def wrapper(func_or_arg=None):
            wrapper_parameter_arg = args
            wrapper_parameter_kwargs = kwargs

            obj = instantiate(func_or_arg, *args, **kwargs)
            return obj

        def instantiate(*args, **kwargs):
            dic = dict(broker_url=self.broker_url, queue_name=self.queue_name)

            for key, item in kwargs.items():
                if key in dic:
                    raise Exception("coordinatorから受け取った値と重複しています。 key: {}".format(key))
                dic[key] = item

            obj = DelayTask(*args, **dic)
            self.tasks[obj.func_name] = obj

            return obj

        # カッコ省略の場合(第一引数が関数)
        if callable(func_or_arg) and len(args) == 0 and len(kwargs) == 0:
            obj = wrapper(func_or_arg)
            # obj = instantiate(func_or_arg, *args, **kwargs)
            return obj

        else:
            # 引数を保持した関数を返す
            return wrapper

    def get_consumer(self):
        from rabbitmq import Consumer

        consumer = Consumer(
            broker_url=self.broker_url,
            queue_name=self.queue_name,
            durable=self.durable,
            tasks=self.get_tasks(),
            auto_ack=self.auto_ack,
            inactivity_timeout=1,
        )

        return consumer
