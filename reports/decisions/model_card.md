# SentinelX Decision Engine

## Decision States

- APPROVE
- REVIEW
- BLOCK

## Prototype Policy

| Risk Score | Decision |
|---:|---|
| < 30 | APPROVE |
| 30 - < 60 | REVIEW |
| >= 60 | BLOCK |

These thresholds are prototype policy values and must be calibrated against validation data, false-positive cost, false-negative cost and analyst review capacity.

## Alerting

REVIEW and BLOCK decisions create an alert.

Each alert receives:

- Alert ID
- Case ID
- Severity
- Decision
- Risk score
- Explanation
- OPEN status

## Auditability

Every decision stores:

- transaction_id
- risk_score
- decision
- severity
- model_version
- rule_version
- policy_version
