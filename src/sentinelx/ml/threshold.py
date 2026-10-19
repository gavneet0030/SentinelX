from __future__ import annotations

import pandas as pd

from sklearn.metrics import precision_score, recall_score, f1_score


def optimize_threshold(y_true, probabilities, min_recall=0.50):
    """Rank thresholds for fraud detection using validation data only.

    Prefer maximum precision among thresholds meeting min_recall.
    If none meet the target, prefer maximum recall, then precision.
    """
    results = []

    for threshold in [i / 100 for i in range(5, 96, 5)]:
        predictions = (probabilities >= threshold).astype(int)

        results.append(
            {
                "threshold": threshold,
                "precision": precision_score(
                    y_true, predictions, zero_division=0
                ),
                "recall": recall_score(
                    y_true, predictions, zero_division=0
                ),
                "f1": f1_score(
                    y_true, predictions, zero_division=0
                ),
            }
        )

    frame = pd.DataFrame(results)
    eligible = frame[frame["recall"] >= min_recall]

    if not eligible.empty:
        # Meet the recall target first, then maximize precision.
        return eligible.sort_values(
            ["precision", "recall", "threshold"],
            ascending=[False, False, False],
            kind="mergesort",
        ).reset_index(drop=True)

    # If the target is unattainable, preserve recall as the priority.
    return frame.sort_values(
        ["recall", "precision", "f1", "threshold"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)
