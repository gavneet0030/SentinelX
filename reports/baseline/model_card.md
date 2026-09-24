# SentinelX Baseline Fraud Detection Model Card


## Purpose

This model identifies potentially fraudulent transactions
from transaction history.


## Models

- Logistic Regression baseline
- XGBoost baseline


## Data

Development dataset:

- Synthetic transaction data
- Chronological split
- Train / Validation / Test separation


## Features

Transaction:

- amount
- transaction time
- payment method
- channel


Behavior:

- previous customer transaction count
- customer historical amount
- merchant activity
- device activity


## Evaluation

Metrics:

- Precision
- Recall
- F1-score
- ROC-AUC
- PR-AUC


## Limitations

This model is trained on synthetic development data.

Performance does not represent production fraud
detection capability.

Real deployment requires:

- production transaction streams
- monitoring
- retraining
- human feedback loops
