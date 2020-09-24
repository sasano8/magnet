import asyncio
import json
import logging
import pika

from rabbitmq.task import DelayTask
from rabbitmq.schemas import Message, FunctionWrapper

logger = logging.getLogger("rabbitmq")
logger.setLevel("INFO")


class Consumer:
    def __init__(
        self,
        broker_url=None,
        queue_name="default",
        tasks={},
        durable=True,
        auto_ack=False,
        inactivity_timeout=1,
        timeout_when_connection_close = 10
    ):

        self.broker_url = broker_url
        self._connection = None
        self.queue_name = queue_name
        self.tasks = tasks
        self.durable = durable
        self.auto_ack = auto_ack
        self.inactivity_timeout = inactivity_timeout

        self._is_interrupted = False
        self.main_task = None
        # self.current_task = asyncio.create_task(asyncio.sleep(0.1))

    def startup(self):
        logger.info("consumer initializing...")
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
        logger.info("consumer handle exit.")

        self._is_interrupted = True

        if self.main_task:
            self.main_task.cancel()
        # self.stop()

    def stop(self):
        self._is_interrupted = True
        conn = self.get_connection()

        if conn.is_closed:
            return

        logger.info("consumer shutting down")
        conn.close()

    def get_connection(self):
        if not self._connection:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.broker_url)
            )

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
            logger.info("consumer success to connect server.")
        else:
            logger.error("consumer failed to connect server.")

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
            self.main_task = asyncio.create_task(self.main_loop(channel))
            await self.main_task

        self.stop()


    async def main_loop(self, channel):
        logger.info("consumer start to consume.")

        """channelから無限にキューを取り出す"""
        for message in channel.consume(
            self.queue_name,
            inactivity_timeout=self.inactivity_timeout,
            auto_ack=self.auto_ack,
        ):
            if self._is_interrupted:
                break

            no_message = not any(message)

            # キューがない時は空が返る
            if no_message:
                # await asyncio.sleep(1)
                self.current_task = asyncio.create_task(asyncio.sleep(1))
                # continue

            else:
                method, properties, body = message
                body = json.loads(body)
                task = self.on_callback(channel, method, properties, body)
                self.current_task = asyncio.create_task(task)

            await self.current_task


    async def on_callback(self, channel, method, properties, body):
        await asyncio.sleep(0)
        logger.info("RECEIVE %r" % body)

        try:
            msg = Message(**body)

            if msg.func in self.tasks:
                task = self.tasks[msg.func]
            else:
                raise Exception(f"Not found function: {msg.func}")

            if task.func_type == FunctionWrapper.FuncType.ASYNC:
                # TODO: auto_ackでラップしてあげないと、完了したのにフラグが立たない可能性がある
                await task.consume(msg)
            else:
                task.consume(msg)

            logger.info("COMPLETE %r" % body)
            if self.auto_ack == False:
                # 処理完了を応答し、メッセージを削除する
                channel.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            logging.exception(f"{body}")
            # TODO: 処理が数回失敗した場合は、デッドレターキューに格納する（現在はとりあえず削除）
            channel.basic_ack(delivery_tag=method.delivery_tag)

