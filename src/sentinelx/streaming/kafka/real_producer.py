from __future__ import annotations

import json

from confluent_kafka import Producer

from sentinelx.streaming.kafka.config import KafkaConfig
from sentinelx.streaming.schemas.message import StreamMessage


class KafkaProducerClient:

    def __init__(
        self,
        config: KafkaConfig | None = None,
    ):
        self.config = config or KafkaConfig()

        self.producer = Producer(
            {
                "bootstrap.servers": self.config.bootstrap_servers,
                "client.id": self.config.client_id,
                "acks": self.config.acks,
                "retries": self.config.retries,
                "delivery.timeout.ms": self.config.delivery_timeout_ms,
            }
        )

    def publish(
        self,
        topic: str,
        message: StreamMessage,
    ) -> None:

        payload = json.dumps(
            {
                "event_id": message.event_id,
                "event_type": message.event_type,
                "payload": message.payload,
                "timestamp": message.timestamp,
            }
        ).encode("utf-8")

        self.producer.produce(
            topic=topic,
            key=message.event_id,
            value=payload,
        )

        self.producer.poll(0)

    def flush(self) -> int:
        return self.producer.flush()
