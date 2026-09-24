from sentinelx.streaming.kafka.memory_broker import (
    InMemoryBroker,
)

from sentinelx.streaming.kafka.producer import (
    StreamProducer,
)

from sentinelx.streaming.kafka.consumer import (
    StreamConsumer,
)

from sentinelx.streaming.kafka.topics import (
    KafkaTopics,
)

from sentinelx.streaming.schemas.message import (
    create_message,
)

from sentinelx.streaming.dlq.queue import (
    DeadLetterQueue,
)


def main():

    topics = KafkaTopics()

    broker = InMemoryBroker()

    producer = StreamProducer(
        broker
    )

    dlq = DeadLetterQueue()


    # --------------------------------------------------------
    # Generate demo streaming events
    # --------------------------------------------------------

    for i in range(10):

        message = create_message(
            event_id=f"stream-{i:04d}",

            event_type=
                "transaction",

            payload={
                "transaction_id":
                    f"tx-{i:04d}",

                "amount":
                    100 + i,

                "currency":
                    "USD",
            },
        )

        producer.publish(
            topics.transactions_raw,
            message,
        )


    # --------------------------------------------------------
    # Consumer
    # --------------------------------------------------------

    consumer = StreamConsumer(
        broker,
        topics.transactions_raw,
    )


    validated = 0


    def process(message):

        nonlocal validated

        try:

            if not message.event_id:
                raise ValueError(
                    "Missing event ID"
                )

            producer.publish(
                topics.transactions_validated,
                message,
            )

            validated += 1

        except Exception as exc:

            dlq.push(
                message.event_id,
                str(exc),
                message.payload,
            )


    processed = consumer.process(
        process
    )


    print()
    print(
        "Raw events:",
        processed,
    )

    print(
        "Validated events:",
        validated,
    )

    print(
        "DLQ events:",
        dlq.size(),
    )

    print(
        "Validated topic:",
        broker.size(
            topics.transactions_validated
        ),
    )

    print()
    print(
        "STREAMING PIPELINE COMPLETE"
    )


if __name__ == "__main__":

    main()
