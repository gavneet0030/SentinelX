# SentinelX Risk and Decision Policy

## Decision Outputs
- APPROVE
- REVIEW
- BLOCK

## Evidence Sources
The intended risk engine can combine:
- Model scores
- Rule signals
- Anomaly scores
- Behavioral and temporal features
- Graph signals, when supported by the data

## Risk Aggregation
The aggregation method must be explicitly defined and tested.
Do not treat illustrative scores or weights as validated production values.

## Thresholds
Decision thresholds should be configurable and evaluated against validation data
and the costs of false positives and false negatives.

## Explainability
Each decision should expose the available supporting evidence.
Do not generate explanations that claim evidence the system did not calculate.

## Auditability
Where implemented, record the event identifier, decision, score,
model version, feature version and timestamp.

## Implementation Status
Final thresholds and production behavior remain subject to implementation and evaluation.
