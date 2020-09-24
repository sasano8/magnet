from rabbitmq import RabbitApp

rabbitmq = RabbitApp(
    broker_url="rabbitmq",
    queue_name="default",
    auto_ack=False,
    durable=True,
    queue_delete=True,
)

