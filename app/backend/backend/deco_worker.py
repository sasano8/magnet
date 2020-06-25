from rabbitmq import TaskFactory

worker = TaskFactory(broker_url="rabbitmq", queue_name="default", auto_ack=False, durable=True, queue_delete=True)

@worker.task
def hello(msg: str = None):
    """文字列を書き出すだけの関数"""
    print('hello {}'.format(msg))


@worker.task
def add(a, b):
    """文字列を書き出すだけの関数"""
    print('result: {}'.format(a + b))

@worker.task()
def add2(a, b):
    """文字列を書き出すだけの関数"""
    print('result: {}'.format((a + b) * 2))

@worker.task(name="test")
def add3(a, b):
    """文字列を書き出すだけの関数"""
    print('result: {}'.format((a + b) * 3))

from uvicorn.protocols.http.httptools_impl import httptools_impl
