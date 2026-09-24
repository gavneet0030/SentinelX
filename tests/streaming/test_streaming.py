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
    serialize_message,
    deserialize_message,
)

from sentinelx.streaming.dlq.queue import (
    DeadLetterQueue,
)


def test_message_roundtrip():

    message = create_message(
        "evt-1",
        "transaction",
        {
            "amount": 100,
        },
    )

    encoded = serialize_message(
        message
    )

    decoded = deserialize_message(
        encoded
    )

    assert decoded.event_id == "evt-1"
    assert decoded.event_type == "transaction"
    assert decoded.payload["amount"] == 100


def test_producer_consumer():

    broker = InMemoryBroker()

    producer = StreamProducer(
        broker
    )

    topics = KafkaTopics()

    message = create_message(
        "evt-2",
        "transaction",
        {},
    )

    producer.publish(
        topics.transactions_raw,
        message,
    )

    consumer = StreamConsumer(
        broker,
        topics.transactions_raw,
    )

    received = consumer.poll()

    assert received is not None
    assert received.event_id == "evt-2"


def test_consumer_handler():

    broker = InMemoryBroker()

    producer = StreamProducer(
        broker
    )

    topics = KafkaTopics()

    for i in range(3):

        producer.publish(
            topics.transactions_raw,

            create_message(
                f"evt-{i}",
                "transaction",
                {},
            ),
        )


    consumer = StreamConsumer(
        broker,
        topics.transactions_raw,
    )


    received = []

    count = consumer.process(
        lambda message:
            received.append(
                message.event_id
            )
    )


    assert count == 3
    assert len(received) == 3


def test_dlq():

    dlq = DeadLetterQueue()

    dlq.push(
        "evt-bad",
        "validation error",
        {"bad": True},
    )

    assert dlq.size() == 1
    assert dlq.messages[0]["event_id"] == "evt-bad"
