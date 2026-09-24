from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class StreamMessage:

    event_id: str
    event_type: str
    payload: dict[str, Any]
    timestamp: str


def create_message(
    event_id: str,
    event_type: str,
    payload: dict[str, Any],
) -> StreamMessage:

    return StreamMessage(
        event_id=event_id,
        event_type=event_type,
        payload=payload,
        timestamp=datetime.now(
            timezone.utc
        ).isoformat(),
    )


def serialize_message(
    message: StreamMessage,
) -> bytes:

    return json.dumps(
        {
            "event_id":
                message.event_id,

            "event_type":
                message.event_type,

            "payload":
                message.payload,

            "timestamp":
                message.timestamp,
        },
        separators=(",", ":"),
    ).encode("utf-8")


def deserialize_message(
    data: bytes,
) -> StreamMessage:

    obj = json.loads(
        data.decode("utf-8")
    )

    return StreamMessage(
        event_id=obj["event_id"],
        event_type=obj["event_type"],
        payload=obj["payload"],
        timestamp=obj["timestamp"],
    )
