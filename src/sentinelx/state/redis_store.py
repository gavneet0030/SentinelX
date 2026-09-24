from __future__ import annotations

import json
from typing import Any

import redis

from sentinelx.state.redis_config import RedisConfig


class RedisStateStore:

    def __init__(
        self,
        config: RedisConfig | None = None,
    ):

        self.config = config or RedisConfig()

        self.client = redis.Redis(
            host=self.config.host,
            port=self.config.port,
            db=self.config.db,
            decode_responses=self.config.decode_responses,
            socket_timeout=self.config.socket_timeout,
            socket_connect_timeout=self.config.socket_connect_timeout,
        )


    def ping(self) -> bool:

        return bool(self.client.ping())


    def set_json(
        self,
        key: str,
        value: dict[str, Any],
        ttl_seconds: int | None = None,
    ) -> None:

        payload = json.dumps(
            value,
            separators=(",", ":"),
        )

        self.client.set(
            key,
            payload,
            ex=ttl_seconds,
        )


    def get_json(
        self,
        key: str,
    ) -> dict[str, Any] | None:

        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)


    def delete(
        self,
        key: str,
    ) -> int:

        return int(
            self.client.delete(key)
        )


    def increment(
        self,
        key: str,
        amount: int = 1,
        ttl_seconds: int | None = None,
    ) -> int:

        value = int(
            self.client.incrby(
                key,
                amount,
            )
        )

        if ttl_seconds is not None and value == amount:

            self.client.expire(
                key,
                ttl_seconds,
            )

        return value


    def exists(
        self,
        key: str,
    ) -> bool:

        return bool(
            self.client.exists(key)
        )


    def close(self) -> None:

        self.client.close()
