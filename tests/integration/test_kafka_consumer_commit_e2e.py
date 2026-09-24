import time
import uuid

from sentinelx.streaming.kafka.config import KafkaConfig
from sentinelx.streaming.kafka.real_producer import KafkaProducerClient
from sentinelx.streaming.kafka.real_consumer import KafkaConsumerClient
from sentinelx.streaming.schemas.message import StreamMessage


TOPIC = "transactions.raw"


def main():

    config = KafkaConfig(
        group_id=f"sentinelx-e2e-{uuid.uuid4().hex[:8]}"
    )

    producer = KafkaProducerClient(config)
    consumer = KafkaConsumerClient(
        topics=[TOPIC],
        config=config,
    )

    event_id = "kafka_e2e_" + uuid.uuid4().hex[:12]

    message = StreamMessage(
        event_id=event_id,
        event_type="transaction.created",
        payload={
            "transaction_id": event_id,
            "customer_id": "kafka_customer_001",
            "merchant_id": "kafka_merchant_001",
            "amount": 425.75,
            "currency": "USD",
        },
        timestamp="2026-09-20T10:30:00Z",
    )

    try:

        producer.publish(
            topic=TOPIC,
            message=message,
        )

        remaining = producer.flush()

        assert remaining == 0

        print("[PASS] Producer published message")
        print("[PASS] Kafka delivery completed")

        received = None
        deadline = time.time() + 15

        while time.time() < deadline:

            result = consumer.poll(timeout=1.0)

            if result is None:
                continue

            stream_message, kafka_message = result

            if stream_message.event_id == event_id:
                received = (
                    stream_message,
                    kafka_message,
                )
                break

        assert received is not None

        stream_message, kafka_message = received

        assert stream_message.event_id == event_id
        assert stream_message.event_type == "transaction.created"
        assert (
            stream_message.payload["transaction_id"]
            == event_id
        )

        print("[PASS] Consumer received message")
        print("[PASS] StreamMessage deserialization")

        consumer.commit(kafka_message)

        print("[PASS] Manual Kafka offset commit")

        print("")
        print("============================================================")
        print(" PHASE 11 BLOCK 1 PASSED")
        print("============================================================")

    finally:
        consumer.close()


if __name__ == "__main__":
    main()
