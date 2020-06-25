import json
import pika
import asyncio


class Consumer:
    def __init__(self, broker_url=None, queue_name="default", tasks={}, durable=True, auto_ack=False, inactivity_timeout=1,
                 on_should_reload=None):

        self.broker_url = broker_url
        self._connection = None
        self.queue_name = queue_name
        self.tasks = tasks
        self.durable = durable
        self.auto_ack = auto_ack
        self.inactivity_timeout = inactivity_timeout
        self.on_should_reload = on_should_reload if on_should_reload else \
            lambda : False

        self._is_interrupted = False


    def stop(self):
        self._is_interrupted = True
        conn = self.get_connection()

        if conn.is_closed:
            return

        conn.close()

    def get_connection(self):
        if not self._connection:
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(
            self.broker_url))

        return self._connection

    async def run(self):

        count = 0

        while True:
            print("initialize thread.")
            count += 1
            await asyncio.sleep(1)
            if hasattr(self, "_is_interrupted"):
                break

            if count > 30:
                raise Exception("初期化に失敗しました")

        connection = self.get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=self.durable)

        print("start subscribe.")


        for message in channel.consume(self.queue_name, inactivity_timeout=self.inactivity_timeout,
                                       auto_ack=self.auto_ack):

            if self.on_should_reload():
                break

            if self._is_interrupted:
                break

            exist_value = any(message)

            if not exist_value:
                await asyncio.sleep(1)
                continue

            method, properties, body = message
            # print(body)
            body = json.loads(body)
            self.on_callback(channel, method, properties, body)

            await asyncio.sleep(0.1)

        self.stop()

    def on_callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

        # body = json.loads(body)

        func_name = body["func"]
        args = body.get("args", [])
        kwargs = body.get("kwargs", {})

        # consumer = self._producers[func_name]
        consumer = self.tasks[func_name]
        consumer(*args, **kwargs)

        print(" [x] completed %r" % body)
        if self.auto_ack == False:
            # 処理完了を応答し、メッセージを削除する
            ch.basic_ack(delivery_tag=method.delivery_tag)
