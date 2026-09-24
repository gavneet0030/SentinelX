from dataclasses import dataclass


@dataclass(frozen=True)
class RedisConfig:

    host: str = "localhost"

    port: int = 6380

    db: int = 0

    decode_responses: bool = True

    socket_timeout: float = 2.0

    socket_connect_timeout: float = 2.0

