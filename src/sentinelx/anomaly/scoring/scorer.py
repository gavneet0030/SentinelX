"""Anomaly score normalization and classification."""

from __future__ import annotations

import numpy as np
import pandas as pd


def minmax_normalize(
    values: pd.Series | np.ndarray,
) -> np.ndarray:
    values = np.asarray(values, dtype=float)

    minimum = np.nanmin(values)
    maximum = np.nanmax(values)

    if not np.isfinite(minimum) or not np.isfinite(maximum):
        return np.zeros(len(values), dtype=float)

    if maximum - minimum <= 1e-12:
        return np.zeros(len(values), dtype=float)

    normalized = (
        (values - minimum)
        / (maximum - minimum)
    )

    return np.clip(normalized, 0.0, 1.0)


def classify_anomaly(
    score: np.ndarray,
    review_threshold: float = 0.70,
    critical_threshold: float = 0.90,
) -> np.ndarray:
    labels = np.full(
        len(score),
        "NORMAL",
        dtype=object,
    )

    labels[score >= review_threshold] = "REVIEW"
    labels[score >= critical_threshold] = "CRITICAL"

    return labels


def build_anomaly_output(
    frame: pd.DataFrame,
    raw_scores: np.ndarray,
) -> pd.DataFrame:
    result = frame.copy()

    normalized = minmax_normalize(raw_scores)

    result["anomaly_raw_score"] = raw_scores
    result["anomaly_score"] = normalized
    result["anomaly_decision"] = classify_anomaly(
        normalized
    )

    result["anomaly_rank_percentile"] = (
        pd.Series(normalized)
        .rank(method="average", pct=True)
        .to_numpy()
    )

    result["anomaly_signal"] = (
        result["anomaly_score"] >= 0.70
    ).astype(int)

    return result
