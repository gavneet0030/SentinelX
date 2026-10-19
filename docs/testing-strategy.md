# SentinelX Testing Strategy

## Test Layers
1. Unit tests: feature calculations, rules, risk scores and decisions.
2. Data tests: schemas, types, ranges, duplicates and temporal consistency.
3. Model tests: fitting, loading, prediction shape and probability bounds.
4. API tests: endpoint responses, input validation and error handling.
5. Integration tests: Kafka, Redis, PostgreSQL and NexusFlow interactions.
6. End-to-end tests: event ingestion through persistence of a risk decision.
7. Load tests: throughput, latency, resource usage and error rate.
8. Stress and failure tests: overload, dependency outages and recovery.
9. Regression tests: detect unintended changes in model or system behavior.

## Execution Principles
- Keep independent unit tests runnable without external services when possible.
- Mark tests requiring infrastructure clearly.
- Record actual results and environment details.
- Never report planned tests as passing tests.
- Measure performance rather than inventing throughput or latency claims.

## Current Known Checkpoint
- 54 tests were collected in a previous pytest collection run.
- Five tests under tests/unit passed in a separate run.
- Twelve tests across tests/data, tests/decision and tests/alerts passed in a separate run.
- The complete suite has not yet been confirmed passing.
