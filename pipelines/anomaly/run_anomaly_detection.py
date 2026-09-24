"""SentinelX Phase 4 anomaly detection pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from sentinelx.anomaly.features.builder import (
    build_anomaly_features,
)
from sentinelx.anomaly.models.isolation_forest import (
    AnomalyModelConfig,
    IsolationForestAnomalyModel,
)
from sentinelx.anomaly.scoring.scorer import (
    build_anomaly_output,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "transactions.parquet"
)

OUTPUT_DIR = (
    PROJECT_ROOT /
    "reports" /
    "anomaly"
)

MODEL_DIR = (
    PROJECT_ROOT /
    "models" /
    "anomaly"
)

FEATURE_OUTPUT = OUTPUT_DIR / "anomaly_features.parquet"
RESULT_OUTPUT = OUTPUT_DIR / "anomaly_scores.parquet"
CSV_OUTPUT = OUTPUT_DIR / "anomaly_scores.csv"
SUMMARY_OUTPUT = OUTPUT_DIR / "anomaly_summary.json"
MODEL_OUTPUT = MODEL_DIR / "isolation_forest.joblib"


def run() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 60)
    print("SENTINELX ? PHASE 4 ANOMALY DETECTION")
    print("=" * 60)

    print()
    print("[1/6] Loading transactions...")

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {INPUT_PATH}"
        )

    df = pd.read_parquet(INPUT_PATH)

    print(f"Transactions: {len(df):,}")

    print()
    print("[2/6] Building point-in-time-safe features...")

    feature_result = build_anomaly_features(df)

    features = feature_result.frame
    feature_columns = feature_result.feature_columns

    print(f"Features: {len(feature_columns)}")

    features.to_parquet(
        FEATURE_OUTPUT,
        index=False,
    )

    print(f"Saved: {FEATURE_OUTPUT}")

    print()
    print("[3/6] Preparing chronological training data...")

    features = features.sort_values(
        ["timestamp", "transaction_id"]
    ).reset_index(drop=True)

    split_index = int(len(features) * 0.70)

    train = features.iloc[:split_index].copy()
    evaluation = features.iloc[split_index:].copy()

    print(f"Training rows:   {len(train):,}")
    print(f"Evaluation rows: {len(evaluation):,}")

    print()
    print("[4/6] Training Isolation Forest...")

    config = AnomalyModelConfig(
        contamination=0.03,
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    model = IsolationForestAnomalyModel(
        config=config
    )

    model.fit(
        train,
        feature_columns,
    )

    model.save(MODEL_OUTPUT)

    print(f"Model saved: {MODEL_OUTPUT}")

    print()
    print("[5/6] Scoring all transactions...")

    raw_scores = model.score_samples(features)

    results = build_anomaly_output(
        features,
        raw_scores,
    )

    results.to_parquet(
        RESULT_OUTPUT,
        index=False,
    )

    results.to_csv(
        CSV_OUTPUT,
        index=False,
    )

    print(f"Saved: {RESULT_OUTPUT}")
    print(f"Saved: {CSV_OUTPUT}")

    print()
    print("[6/6] Generating anomaly summary...")

    decision_counts = (
        results["anomaly_decision"]
        .value_counts()
        .to_dict()
    )

    top_anomalies = (
        results[
            [
                "transaction_id",
                "customer_id",
                "merchant_id",
                "timestamp",
                "amount",
                "anomaly_score",
                "anomaly_decision",
            ]
        ]
        .sort_values(
            "anomaly_score",
            ascending=False,
        )
        .head(20)
    )

    summary = {
        "dataset": {
            "input": str(INPUT_PATH),
            "rows": int(len(results)),
        },
        "model": {
            "algorithm": "IsolationForest",
            "n_estimators": config.n_estimators,
            "contamination": config.contamination,
            "random_state": config.random_state,
        },
        "features": {
            "count": len(feature_columns),
            "columns": feature_columns,
        },
        "chronological_split": {
            "training_rows": int(len(train)),
            "evaluation_rows": int(len(evaluation)),
            "training_fraction": 0.70,
        },
        "anomaly_distribution": {
            key: int(value)
            for key, value in decision_counts.items()
        },
        "score_statistics": {
            "min": float(results["anomaly_score"].min()),
            "max": float(results["anomaly_score"].max()),
            "mean": float(results["anomaly_score"].mean()),
            "median": float(results["anomaly_score"].median()),
            "p95": float(results["anomaly_score"].quantile(0.95)),
            "p99": float(results["anomaly_score"].quantile(0.99)),
        },
        "top_anomalies": [
            {
                key: (
                    value.isoformat()
                    if hasattr(value, "isoformat")
                    else (
                        float(value)
                        if hasattr(value, "item")
                        else value
                    )
                )
                for key, value in row.items()
            }
            for row in top_anomalies.to_dict(
                orient="records"
            )
        ],
    }

    SUMMARY_OUTPUT.write_text(
        json.dumps(
            summary,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved: {SUMMARY_OUTPUT}")

    print()
    print("=" * 60)
    print("ANOMALY DETECTION SUMMARY")
    print("=" * 60)

    for key, value in decision_counts.items():
        print(f"{key:10}: {value:,}")

    print()
    print(
        "Average anomaly score:",
        f"{results['anomaly_score'].mean():.4f}",
    )

    print(
        "P95 anomaly score:",
        f"{results['anomaly_score'].quantile(0.95):.4f}",
    )

    print(
        "P99 anomaly score:",
        f"{results['anomaly_score'].quantile(0.99):.4f}",
    )

    print()
    print("=" * 60)
    print("PHASE 4 PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run()

