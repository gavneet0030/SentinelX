# SentinelX — Threshold Sensitivity Analysis

> Diagnostic analysis on test predictions only. Do not use these results to tune the final threshold.

Each row shows how changing the threshold changes fraud detection and alert workload.

| Model | Threshold | TP | FP | FN | Alerts | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| transaction_baseline | 0.50 | 27 | 423 | 21 | 450 | 6.00% | 56.25% | 0.1084 |
| transaction_baseline | 0.55 | 22 | 342 | 26 | 364 | 6.04% | 45.83% | 0.1068 |
| transaction_baseline | 0.60 | 21 | 271 | 27 | 292 | 7.19% | 43.75% | 0.1235 |
| transaction_baseline | 0.65 | 17 | 213 | 31 | 230 | 7.39% | 35.42% | 0.1223 |
| transaction_baseline | 0.70 | 17 | 151 | 31 | 168 | 10.12% | 35.42% | 0.1574 |
| transaction_baseline | 0.75 | 11 | 107 | 37 | 118 | 9.32% | 22.92% | 0.1325 |
| transaction_baseline | 0.80 | 7 | 65 | 41 | 72 | 9.72% | 14.58% | 0.1167 |
| transaction_baseline | 0.85 | 5 | 33 | 43 | 38 | 13.16% | 10.42% | 0.1163 |
| transaction_baseline | 0.90 | 2 | 11 | 46 | 13 | 15.38% | 4.17% | 0.0656 |
| transaction_baseline | 0.95 | 2 | 1 | 46 | 3 | 66.67% | 4.17% | 0.0784 |
| transaction_temporal | 0.50 | 27 | 427 | 21 | 454 | 5.95% | 56.25% | 0.1076 |
| transaction_temporal | 0.55 | 25 | 341 | 23 | 366 | 6.83% | 52.08% | 0.1208 |
| transaction_temporal | 0.60 | 20 | 263 | 28 | 283 | 7.07% | 41.67% | 0.1208 |
| transaction_temporal | 0.65 | 19 | 212 | 29 | 231 | 8.23% | 39.58% | 0.1362 |
| transaction_temporal | 0.70 | 17 | 153 | 31 | 170 | 10.00% | 35.42% | 0.1560 |
| transaction_temporal | 0.75 | 13 | 104 | 35 | 117 | 11.11% | 27.08% | 0.1576 |
| transaction_temporal | 0.80 | 8 | 65 | 40 | 73 | 10.96% | 16.67% | 0.1322 |
| transaction_temporal | 0.85 | 5 | 34 | 43 | 39 | 12.82% | 10.42% | 0.1149 |
| transaction_temporal | 0.90 | 2 | 11 | 46 | 13 | 15.38% | 4.17% | 0.0656 |
| transaction_temporal | 0.95 | 2 | 1 | 46 | 3 | 66.67% | 4.17% | 0.0784 |
| transaction_behavioral | 0.50 | 30 | 492 | 18 | 522 | 5.75% | 62.50% | 0.1053 |
| transaction_behavioral | 0.55 | 26 | 391 | 22 | 417 | 6.24% | 54.17% | 0.1118 |
| transaction_behavioral | 0.60 | 24 | 320 | 24 | 344 | 6.98% | 50.00% | 0.1224 |
| transaction_behavioral | 0.65 | 19 | 250 | 29 | 269 | 7.06% | 39.58% | 0.1199 |
| transaction_behavioral | 0.70 | 18 | 194 | 30 | 212 | 8.49% | 37.50% | 0.1385 |
| transaction_behavioral | 0.75 | 15 | 144 | 33 | 159 | 9.43% | 31.25% | 0.1449 |
| transaction_behavioral | 0.80 | 8 | 88 | 40 | 96 | 8.33% | 16.67% | 0.1111 |
| transaction_behavioral | 0.85 | 8 | 41 | 40 | 49 | 16.33% | 16.67% | 0.1649 |
| transaction_behavioral | 0.90 | 4 | 17 | 44 | 21 | 19.05% | 8.33% | 0.1159 |
| transaction_behavioral | 0.95 | 2 | 4 | 46 | 6 | 33.33% | 4.17% | 0.0741 |
| full_with_graph | 0.50 | 31 | 498 | 17 | 529 | 5.86% | 64.58% | 0.1075 |
| full_with_graph | 0.55 | 27 | 423 | 21 | 450 | 6.00% | 56.25% | 0.1084 |
| full_with_graph | 0.60 | 24 | 337 | 24 | 361 | 6.65% | 50.00% | 0.1174 |
| full_with_graph | 0.65 | 23 | 257 | 25 | 280 | 8.21% | 47.92% | 0.1402 |
| full_with_graph | 0.70 | 21 | 204 | 27 | 225 | 9.33% | 43.75% | 0.1538 |
| full_with_graph | 0.75 | 15 | 157 | 33 | 172 | 8.72% | 31.25% | 0.1364 |
| full_with_graph | 0.80 | 9 | 104 | 39 | 113 | 7.96% | 18.75% | 0.1118 |
| full_with_graph | 0.85 | 7 | 59 | 41 | 66 | 10.61% | 14.58% | 0.1228 |
| full_with_graph | 0.90 | 5 | 30 | 43 | 35 | 14.29% | 10.42% | 0.1205 |
| full_with_graph | 0.95 | 2 | 9 | 46 | 11 | 18.18% | 4.17% | 0.0678 |
