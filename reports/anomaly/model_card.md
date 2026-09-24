# SentinelX — Isolation Forest Anomaly Model Card

## Model

Algorithm:

**Isolation Forest**

Purpose:

Detect transactions that exhibit unusual behavior relative to the historical
transaction feature distribution.

## Why Isolation Forest?

Isolation Forest is used as the initial unsupervised anomaly detector because:

- It does not require fraud labels.
- It can detect unusual combinations of numerical features.
- It is computationally practical for a first production prototype.
- It provides an independent signal from supervised fraud classification.
- It can be combined later with behavioral, rule, graph and supervised ML signals.

## Feature Families

The current anomaly detector uses:

### Transaction

- amount
- log-transformed amount
- large-amount indicator

### Temporal

- hour
- day of week
- weekend indicator
- night indicator
- time since previous customer transaction
- customer velocity over 1 hour
- customer velocity over 24 hours

### Behavioral

- previous customer transaction count
- previous customer amount sum
- previous customer mean amount
- amount relative to previous transaction
- amount relative to previous customer mean
- customer historical deviation

### Device

- previous device transaction count
- new device for customer

### Merchant

- previous merchant transaction count

### Categorical Encodings

- payment method
- channel
- country

## Leakage Policy

Features intended for anomaly detection must only use information available
at the time the transaction is evaluated.

The feature builder therefore uses:

- chronological ordering
- previous-event statistics
- shifted customer history
- historical velocity windows

Future transactions must not influence the current event's features.

## Model Configuration

Initial configuration:

- contamination: 0.03
- estimators: 300
- random_state: 42
- n_jobs: -1

These are engineering defaults and are not claimed to be optimal.

## Score Interpretation

The raw Isolation Forest score is transformed into an anomaly-oriented score.

Higher normalized score:

**more anomalous**

Initial operational labels:

- NORMAL: score < 0.70
- REVIEW: 0.70 <= score < 0.90
- CRITICAL: score >= 0.90

These thresholds are provisional.

They must eventually be calibrated against:

- review capacity
- false-positive cost
- fraud capture
- analyst workload
- downstream risk aggregation
- production operating characteristics

## Evaluation

Because this is an unsupervised detector, evaluation should not rely only
on model-internal scores.

Future evaluation should include:

- PR-AUC against fraud labels
- ROC-AUC
- precision at review capacity
- recall at review capacity
- precision@K
- recall@K
- false-positive rate
- score stability
- temporal stability
- latency
- feature drift

## Future Work

Potential future improvements:

1. Robust scaling.
2. Model calibration.
3. Threshold optimization.
4. Comparison with Local Outlier Factor.
5. Comparison with One-Class SVM.
6. Ensemble anomaly score.
7. Graph anomaly signals.
8. Temporal anomaly models.
9. Autoencoder only if justified by experiments.
10. Production monitoring and drift detection.

Deep learning is intentionally deferred until simpler approaches are
benchmarked.
