from rabbitmq import RabbitApp

app = RabbitApp(broker_url="rabbitmq", queue_name="default", auto_ack=False, durable=True, queue_delete=True)

@app.task
def hello(msg: str = None):
    """文字列を書き出すだけの関数"""
    print('hello!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {}'.format(msg))


@app.task
def add(a, b):
    """文字列を書き出すだけの関数"""
    print('result:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {}'.format(a + b))

@app.task()
def add2(a, b):
    """文字列を書き出すだけの関数"""
    print('result: {}'.format((a + b) * 2))

# @app.task(name="test") # キーワード引数を渡せることを確認済み
@app.task()
def add3(a, b):
    """文字列を書き出すだけの関数"""
    print('result: {}'.format((a + b) * 3))

