# SentinelX Explainability Model Card

## Purpose

The SentinelX explainability layer provides auditable evidence for risk decisions.

## Evidence Sources

- ML fraud probability
- Behavioral risk
- Anomaly score
- Graph risk
- Shared-device relationships
- Shared-merchant relationships

## Current Output

The explainability pipeline generates:

- Transaction-level risk score
- Risk level
- Evidence count
- Human-readable risk reasons
- Structured evidence JSON

## SHAP

SHAP infrastructure is included for model-level feature attribution.

SHAP values describe model contribution and should not be interpreted as causal effects.

## Evidence Policy

Explanations are generated from observed SentinelX signals.

The system must not fabricate unsupported reasons.

## Current Limitations

- Evidence thresholds are prototype thresholds.
- Risk fusion weights require calibration.
- Graph features require continued validation.
- SHAP attribution is currently available as a separate model-explanation component.
- Production deployment requires monitoring and regression testing.

## Validation

Phase 7 currently validates:

- Evidence generation
- Explanation structure
- Transaction-level explanation output
- Explanation artifact generation
