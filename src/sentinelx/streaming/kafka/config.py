from dataclasses import dataclass


@dataclass(frozen=True)
class KafkaConfig:
    bootstrap_servers: str = "localhost:9092"
    client_id: str = "sentinelx"
    group_id: str = "sentinelx-risk-engine"

    auto_offset_reset: str = "earliest"
    enable_auto_commit: bool = False

    request_timeout_ms: int = 10000
    session_timeout_ms: int = 45000
    max_poll_interval_ms: int = 300000

    acks: str = "all"
    retries: int = 5
    delivery_timeout_ms: int = 120000
