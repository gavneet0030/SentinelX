from __future__ import annotations

from datetime import datetime, timezone


class DeadLetterQueue:

    def __init__(self):

        self.messages = []


    def push(
        self,
        event_id: str,
        error: str,
        payload,
    ):

        self.messages.append(
            {
                "event_id":
                    event_id,

                "error":
                    error,

                "payload":
                    payload,

                "timestamp":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),
            }
        )


    def size(self):

        return len(
            self.messages
        )
