from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_model(
    model,
    X,
    y,
    model_name: str,
    output_dir: str | Path,
    threshold: float = 0.5,
) -> dict:

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    probabilities = model.predict_proba(X)[:, 1]

    predictions = (
        probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y,
        predictions,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y,
        probabilities,
    )

    pr_auc = average_precision_score(
        y,
        probabilities,
    )

    matrix = confusion_matrix(
        y,
        predictions,
    )

    report = classification_report(
        y,
        predictions,
        output_dict=True,
        zero_division=0,
    )

    metrics = {
        "model": model_name,
        "threshold": threshold,
        "sample_count": int(len(y)),
        "positive_count": int(np.sum(y)),
        "negative_count": int(len(y) - np.sum(y)),
        "fraud_rate": float(np.mean(y)),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": float(roc_auc),
        "pr_auc": float(pr_auc),
        "confusion_matrix": matrix.tolist(),
        "classification_report": report,
    }

    metrics_path = output_dir / f"{model_name}_metrics.json"

    with metrics_path.open(
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(
            metrics,
            handle,
            indent=2,
        )

    prediction_frame = pd.DataFrame(
        {
            "actual": np.asarray(y),
            "predicted": predictions,
            "fraud_probability": probabilities,
        }
    )

    prediction_path = (
        output_dir
        / f"{model_name}_predictions.csv"
    )

    prediction_frame.to_csv(
        prediction_path,
        index=False,
    )

    return metrics
