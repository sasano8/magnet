import json
import pika
import asyncio
from rabbitmq import DelayTask

class Consumer:
    def __init__(self, broker_url=None, queue_name="default", tasks={}, durable=True, auto_ack=False, inactivity_timeout=1):

        self.broker_url = broker_url
        self._connection = None
        self.queue_name = queue_name
        self.tasks = tasks
        self.durable = durable
        self.auto_ack = auto_ack
        self.inactivity_timeout = inactivity_timeout

        self._is_interrupted = False

    def startup(self):
        print("consumer initializing...")
        self.install_signal_handlers()

    def install_signal_handlers(self):
        import signal
        HANDLED_SIGNALS = (
            signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
            signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
        )

        # TODO: modify get_running_loop
        loop = asyncio.get_event_loop()

        try:
            for sig in HANDLED_SIGNALS:
                loop.add_signal_handler(sig, self.handle_exit, sig, None)
        except NotImplementedError:
            # Windows
            for sig in HANDLED_SIGNALS:
                signal.signal(sig, self.handle_exit)

    def handle_exit(self, sig, frame):
        self.stop()


    def stop(self):
        self._is_interrupted = True
        conn = self.get_connection()

        if conn.is_closed:
            return

        print("consumer shutting down")
        conn.close()

    def get_connection(self):
        if not self._connection:
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(
            self.broker_url))

        return self._connection

    def try_connect(self):
        result = True

        try:
            conn = self.get_connection()
            if conn.is_closed:
                self._connection = None

        except Exception as e:
            result = False

        if result:
            print("consumer success to connect server.")
        else:
            print("consumer failed to connect server.")

        return result

    async def consume(self):
        self.startup()

        while True:
            if self._is_interrupted:
                break

            if not self.try_connect():
                await asyncio.sleep(1)
                continue

            connection = self.get_connection()
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name, durable=self.durable)

          # TODO: connection切れとRPC失敗の例外処理をする
            await self.main_loop(channel)

        self.stop()

    async def main_loop(self, channel):
        print("consumer start to consume.")

        """channelから無限にキューを取り出す"""
        for message in channel.consume(self.queue_name, inactivity_timeout=self.inactivity_timeout,
                                       auto_ack=self.auto_ack):

            no_message = not any(message)

            # キューがない時は空が返る
            if no_message:
                await asyncio.sleep(1)
                continue

            method, properties, body = message
            body = json.loads(body)
            await self.on_callback(channel, method, properties, body)


    async def on_callback(self, channel, method, properties, body):
        print(" [x] Received %r" % body)

        func_name = body["func"]
        args = body.get("args", [])
        kwargs = body.get("kwargs", {})

        # consumer = self._producers[func_name]
        consumer = self.tasks[func_name]
        if consumer.func_type == DelayTask.FuncType.NORMAL:
            consumer(*args, **kwargs)
        else:
            # TODO: auto_ackでラップしてあげないと、完了したのにフラグが立たない可能性がある
            await consumer(*args, **kwargs)

        print(" [x] completed %r" % body)
        if self.auto_ack == False:
            # 処理完了を応答し、メッセージを削除する
            channel.basic_ack(delivery_tag=method.delivery_tag)

