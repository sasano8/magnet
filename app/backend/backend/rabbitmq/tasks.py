import pika
import json
import copy

class TaskFactory:

    def __init__(self, broker_url, queue_name, auto_ack, durable, queue_delete):
        self.broker_url = broker_url
        self.queue_name = queue_name
        self.auto_ack = auto_ack
        self.durable = durable
        self.queue_delete = queue_delete
        self.tasks = {}
        
    def get_tasks(self):
        return copy.copy(self.tasks)


    def task(self, func_or_arg=None, *args, **kwargs):

        def wrapper(func_or_arg=None):
            wrapper_parameter_arg = args
            wrapper_parameter_kwargs = kwargs

            obj = instantiate(func_or_arg, *args, **kwargs)
            return obj

        def instantiate(*args, **kwargs):
            dic = dict(
                manager=self
            )

            for key, item in kwargs.items():
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


class DelayTask:
    def __init__(self, func, manager: TaskFactory, **kwargs):
        self._func = func
        self.manager = manager

        self.func_name = func.__name__


    def get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(self.manager.broker_url))

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
                              routing_key=self.manager.queue_name,
                              body=body)

        connection.close()


    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


