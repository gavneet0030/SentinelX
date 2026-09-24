from __future__ import annotations

import json

from confluent_kafka import Consumer, KafkaException

from sentinelx.streaming.kafka.config import KafkaConfig
from sentinelx.streaming.schemas.message import StreamMessage


class KafkaConsumerClient:

    def __init__(
        self,
        topics: list[str],
        config: KafkaConfig | None = None,
    ):
        self.config = config or KafkaConfig()

        self.consumer = Consumer(
            {
                "bootstrap.servers": self.config.bootstrap_servers,
                "group.id": self.config.group_id,
                "auto.offset.reset": self.config.auto_offset_reset,
                "enable.auto.commit": self.config.enable_auto_commit,
                "session.timeout.ms": self.config.session_timeout_ms,
                "max.poll.interval.ms": self.config.max_poll_interval_ms,
            }
        )

        self.consumer.subscribe(topics)

    def poll(
        self,
        timeout: float = 1.0,
    ):

        message = self.consumer.poll(timeout)

        if message is None:
            return None

        if message.error():
            raise KafkaException(message.error())

        payload = json.loads(
            message.value().decode("utf-8")
        )

        stream_message = StreamMessage(
            event_id=payload["event_id"],
            event_type=payload["event_type"],
            payload=payload["payload"],
            timestamp=payload["timestamp"],
        )

        return stream_message, message

    def commit(self, message) -> None:
        self.consumer.commit(
            message=message,
            asynchronous=False,
        )

    def close(self) -> None:
        self.consumer.close()
