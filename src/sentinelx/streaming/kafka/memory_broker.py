from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


class InMemoryBroker:

    def __init__(self):

        self.topics = defaultdict(
            deque
        )


    def publish(
        self,
        topic: str,
        message: Any,
    ) -> None:

        self.topics[
            topic
        ].append(message)


    def consume(
        self,
        topic: str,
    ):

        if not self.topics[topic]:
            return None

        return self.topics[
            topic
        ].popleft()


    def size(
        self,
        topic: str,
    ) -> int:

        return len(
            self.topics[topic]
        )
