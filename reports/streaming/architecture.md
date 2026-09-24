# SentinelX Streaming Architecture

## Kafka Topics

- `transactions.raw`
- `transactions.validated`
- `features.generated`
- `risk.decisions`
- `risk.alerts`
- `analyst.feedback`
- `transactions.dlq`

## Flow

Producer
→ transactions.raw
→ Validation
→ transactions.validated
→ Feature/Risk Processing
→ risk.decisions
→ risk.alerts

Invalid events are routed to the dead-letter queue.

## Current Implementation

Phase 9 initially provides an in-memory broker abstraction for deterministic testing.

The abstraction is intentionally separated from the business logic so a Kafka-backed implementation can replace the in-memory broker without rewriting the streaming pipeline.

## Production Direction

The production deployment will use Apache Kafka with:

- partitions
- consumer groups
- offsets
- retry policy
- idempotency
- dead-letter topics
- schema validation
- observability
- backpressure
