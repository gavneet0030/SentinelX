from __future__ import annotations

from sentinelx.streaming.kafka.memory_broker import (
    InMemoryBroker,
)

from sentinelx.streaming.schemas.message import (
    StreamMessage,
)


class StreamProducer:

    def __init__(
        self,
        broker: InMemoryBroker,
    ):

        self.broker = broker


    def publish(
        self,
        topic: str,
        message: StreamMessage,
    ) -> None:

        if not message.event_id:
            raise ValueError(
                "event_id is required"
            )

        self.broker.publish(
            topic,
            message,
        )
