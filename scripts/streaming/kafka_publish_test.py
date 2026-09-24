from sentinelx.streaming.kafka.config import KafkaConfig
from sentinelx.streaming.kafka.real_producer import KafkaProducerClient


class DummyMessage:

    event_id="test_001"

    event_type="transaction"

    payload={
        "amount":100,
        "merchant":"demo"
    }

    timestamp="2026-01-01T00:00:00"



producer = KafkaProducerClient(
    KafkaConfig()
)


producer.publish(
    "transactions.raw",
    DummyMessage()
)


producer.flush()


print("[PASS] Message published")
