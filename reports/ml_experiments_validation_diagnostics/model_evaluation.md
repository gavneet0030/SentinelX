# SentinelX — Model Evaluation Report

## Evaluation setup

- Test observations per model: 1500
- Fraud cases in test split: 48
- Threshold selection: validation split, targeting at least 50% fraud recall.
- Test metrics were evaluated separately from threshold selection.

## Model comparison

| Model | Threshold | Validation Recall | Test Precision | Test Recall | Test F1 | Test PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| transaction_baseline | 0.65 | 57.89% | 7.39% | 35.42% | 0.1223 | 0.1117 |
| transaction_temporal | 0.70 | 50.00% | 10.00% | 35.42% | 0.1560 | 0.1115 |
| transaction_behavioral | 0.70 | 52.63% | 8.49% | 37.50% | 0.1385 | 0.1223 |
| full_with_graph | 0.70 | 52.63% | 9.33% | 43.75% | 0.1538 | 0.1036 |

## Findings

- Highest test PR-AUC: **transaction_behavioral** (0.1223).
- Highest test fraud recall: **full_with_graph** (43.75%).
- Highest test precision: **transaction_temporal** (10.00%).

## Limitations

- The test split contains only 48 fraud cases, limiting the precision of recall estimates.
- Validation recall targets do not guarantee equivalent test recall.
- Low precision means many alerts may be legitimate transactions.
- These results alone do not establish production readiness or prove that graph features improve overall ranking quality.

## Recommended next work

1. Inspect false positives and false negatives.
2. Compare alert volumes at candidate thresholds.
3. Test on additional chronological periods.
4. Document model-selection rationale and limitations.
