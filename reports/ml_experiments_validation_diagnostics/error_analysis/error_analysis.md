# SentinelX — Prediction Error Analysis

## Scope and limitations

- Analysis uses the saved test predictions for four models.
- False positives are legitimate transactions predicted as fraud.
- False negatives are fraud transactions predicted as legitimate.
- Prediction files contain no transaction IDs or original features; row numbers below are file positions, not transaction identifiers.

## Model comparison

| Model | TP | FP | TN | FN | Precision | Recall | Error rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| transaction_baseline | 17 | 213 | 1239 | 31 | 7.39% | 35.42% | 16.27% |

### transaction_baseline

- True positives: 17
- False positives: 213
- True negatives: 1239
- False negatives: 31
- Mean predicted fraud probability among false positives: 0.761467
- Mean predicted fraud probability among false negatives: 0.416885

| transaction_temporal | 17 | 153 | 1299 | 31 | 10.00% | 35.42% | 12.27% |

### transaction_temporal

- True positives: 17
- False positives: 153
- True negatives: 1299
- False negatives: 31
- Mean predicted fraud probability among false positives: 0.795264
- Mean predicted fraud probability among false negatives: 0.419173

| transaction_behavioral | 18 | 194 | 1258 | 30 | 8.49% | 37.50% | 14.93% |

### transaction_behavioral

- True positives: 18
- False positives: 194
- True negatives: 1258
- False negatives: 30
- Mean predicted fraud probability among false positives: 0.798005
- Mean predicted fraud probability among false negatives: 0.439458

| full_with_graph | 21 | 204 | 1248 | 27 | 9.33% | 43.75% | 15.40% |

### full_with_graph

- True positives: 21
- False positives: 204
- True negatives: 1248
- False negatives: 27
- Mean predicted fraud probability among false positives: 0.811249
- Mean predicted fraud probability among false negatives: 0.410165

## Interpretation notes

- False-positive probability averages show how confidently the model flagged legitimate transactions.
- False-negative probability averages show how close missed fraud cases were to being flagged.
- These aggregate statistics do not explain causation. Original features and stable transaction identifiers are needed for case-level investigation.
- Row numbers refer to positions in the saved prediction CSV, not original transaction IDs.
