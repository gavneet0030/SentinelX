from __future__ import annotations

import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)


def optimize_threshold(
    y_true,
    probabilities,
):

    results = []

    thresholds = [
        0.10,
        0.20,
        0.30,
        0.40,
        0.50,
    ]


    for threshold in thresholds:

        predictions = (
            probabilities >= threshold
        ).astype(int)


        results.append(
            {
                "threshold": threshold,
                "precision": precision_score(
                    y_true,
                    predictions,
                    zero_division=0,
                ),
                "recall": recall_score(
                    y_true,
                    predictions,
                    zero_division=0,
                ),
                "f1": f1_score(
                    y_true,
                    predictions,
                    zero_division=0,
                ),
            }
        )


    return (
        pd.DataFrame(results)
        .sort_values(
            "f1",
            ascending=False,
        )
    )
