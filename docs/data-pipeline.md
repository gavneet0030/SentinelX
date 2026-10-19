# SentinelX Data Pipeline

## Intended Stages
1. Ingest CSV, JSON, Parquet or supported API data.
2. Validate schemas, types, ranges and required fields.
3. Handle duplicates and invalid records explicitly.
4. Clean data without silently discarding important evidence.
5. Build transaction, behavioral, temporal and supported graph features.
6. Produce events for downstream processing.
7. Send events through the configured streaming workflow.
8. Pass available features to the risk engine.
9. Store decisions and relevant audit metadata.

## Data Leakage Controls
Features used for a prediction must only use information available at prediction time.
Use chronological train, validation and test splits for temporal evaluation.

## Relationship Integrity
Create graph relationships only when supported by the dataset.
Clearly label synthetic relationships when synthetic data is used.

## Failure Handling
Document validation failures, duplicate events, malformed messages,
dead-letter handling and retry behavior.

## Implementation Status
This is the pipeline specification, not proof that every stage is operational.
