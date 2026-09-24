from __future__ import annotations

from collections.abc import Callable

from sentinelx.streaming.kafka.memory_broker import (
    InMemoryBroker,
)


class StreamConsumer:

    def __init__(
        self,
        broker: InMemoryBroker,
        topic: str,
    ):

        self.broker = broker
        self.topic = topic


    def poll(self):

        return self.broker.consume(
            self.topic
        )


    def process(
        self,
        handler: Callable,
    ):

        processed = 0

        while True:

            message = self.poll()

            if message is None:
                break

            handler(message)

            processed += 1

        return processed
