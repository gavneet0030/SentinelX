from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sentinelx.ml.dataset import time_based_split
from sentinelx.ml.evaluate import evaluate_model
from sentinelx.ml.features import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_features,
)
from sentinelx.ml.models import (
    build_logistic_model,
    build_xgboost_model,
)


DATA_PATH = (
    ROOT
    / "data"
    / "processed"
    / "transactions.parquet"
)

MODEL_ROOT = ROOT / "models"

REPORT_ROOT = (
    ROOT
    / "reports"
    / "baseline"
)


def prepare_xy(frame: pd.DataFrame):
    feature_columns = (
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
    )

    X = frame[feature_columns].copy()

    y = (
        frame["is_fraud"]
        .astype(int)
        .copy()
    )

    return X, y


def print_split_info(name, frame):
    fraud_count = int(
        frame["is_fraud"].sum()
    )

    fraud_rate = (
        fraud_count / len(frame)
        if len(frame)
        else 0
    )

    print(
        f"{name:<12}"
        f" rows={len(frame):>6}"
        f" fraud={fraud_count:>5}"
        f" rate={fraud_rate:.4f}"
    )

    if len(frame):
        print(
            f"  time: "
            f"{frame['timestamp'].min()} "
            f"-> "
            f"{frame['timestamp'].max()}"
        )


def train_one(
    name,
    model,
    train_x,
    train_y,
    test_x,
    test_y,
):
    print("")
    print("=" * 60)
    print(f" TRAINING {name.upper()}")
    print("=" * 60)

    model.fit(
        train_x,
        train_y,
    )

    metrics = evaluate_model(
        model=model,
        X=test_x,
        y=test_y,
        model_name=name,
        output_dir=REPORT_ROOT,
    )

    model_dir = (
        MODEL_ROOT
        / name
    )

    model_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = (
        model_dir
        / "model.joblib"
    )

    joblib.dump(
        model,
        model_path,
    )

    print("")
    print(f"Model saved: {model_path}")
    print("")
    print("Measured test metrics:")
    print(
        f"Precision : {metrics['precision']:.6f}"
    )
    print(
        f"Recall    : {metrics['recall']:.6f}"
    )
    print(
        f"F1        : {metrics['f1']:.6f}"
    )
    print(
        f"ROC-AUC   : {metrics['roc_auc']:.6f}"
    )
    print(
        f"PR-AUC    : {metrics['pr_auc']:.6f}"
    )

    return metrics


def main():
    print("")
    print("=" * 60)
    print(" SENTINELX BASELINE FRAUD ML")
    print("=" * 60)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}"
        )

    print("")
    print("Loading processed dataset...")
    raw = pd.read_parquet(DATA_PATH)

    print(
        f"Loaded {len(raw):,} transactions."
    )

    print("")
    print("Building leakage-safe features...")

    featured = build_features(raw)

    print(
        f"Feature rows: {len(featured):,}"
    )

    print("")
    print("Creating chronological split...")

    train, validation, test = time_based_split(
        featured,
        train_ratio=0.70,
        validation_ratio=0.15,
    )

    print("")
    print_split_info(
        "TRAIN",
        train,
    )

    print_split_info(
        "VALIDATION",
        validation,
    )

    print_split_info(
        "TEST",
        test,
    )

    # --------------------------------------------------------
    # Baseline models are trained on train + validation.
    #
    # Validation remains available as a separate chronological
    # partition for future threshold/model selection.
    #
    # For this first baseline, the final evaluation is performed
    # on the untouched test period.
    # --------------------------------------------------------

    train_validation = pd.concat(
        [train, validation],
        ignore_index=True,
    )

    train_x, train_y = prepare_xy(
        train_validation
    )

    test_x, test_y = prepare_xy(
        test
    )

    print("")
    print(
        f"Training rows: {len(train_x):,}"
    )

    print(
        f"Test rows    : {len(test_x):,}"
    )

    logistic = build_logistic_model()

    logistic_metrics = train_one(
        name="logistic_regression",
        model=logistic,
        train_x=train_x,
        train_y=train_y,
        test_x=test_x,
        test_y=test_y,
    )

    xgb = build_xgboost_model()

    xgb_metrics = train_one(
        name="xgboost",
        model=xgb,
        train_x=train_x,
        train_y=train_y,
        test_x=test_x,
        test_y=test_y,
    )

    # --------------------------------------------------------
    # Dataset metadata
    # --------------------------------------------------------

    metadata = {
        "dataset": str(DATA_PATH),
        "total_rows": int(len(featured)),
        "train_rows": int(len(train)),
        "validation_rows": int(len(validation)),
        "test_rows": int(len(test)),
        "feature_count": int(
            len(NUMERIC_FEATURES)
            + len(CATEGORICAL_FEATURES)
        ),
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "split_method": "chronological",
        "train_ratio": 0.70,
        "validation_ratio": 0.15,
        "test_ratio": 0.15,
        "random_seed": 42,
        "note": (
            "Metrics are measured on the synthetic development "
            "dataset and are not real-world fraud detection claims."
        ),
    }

    metadata_path = (
        REPORT_ROOT
        / "dataset_metadata.json"
    )

    with metadata_path.open(
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(
            metadata,
            handle,
            indent=2,
        )

    # --------------------------------------------------------
    # Comparison summary
    # --------------------------------------------------------

    comparison = pd.DataFrame(
        [
            {
                "model": "logistic_regression",
                "precision": logistic_metrics["precision"],
                "recall": logistic_metrics["recall"],
                "f1": logistic_metrics["f1"],
                "roc_auc": logistic_metrics["roc_auc"],
                "pr_auc": logistic_metrics["pr_auc"],
            },
            {
                "model": "xgboost",
                "precision": xgb_metrics["precision"],
                "recall": xgb_metrics["recall"],
                "f1": xgb_metrics["f1"],
                "roc_auc": xgb_metrics["roc_auc"],
                "pr_auc": xgb_metrics["pr_auc"],
            },
        ]
    )

    comparison_path = (
        REPORT_ROOT
        / "model_comparison.csv"
    )

    comparison.to_csv(
        comparison_path,
        index=False,
    )

    print("")
    print("=" * 60)
    print(" MODEL COMPARISON")
    print("=" * 60)
    print("")
    print(
        comparison.to_string(
            index=False,
            float_format=lambda value: f"{value:.6f}",
        )
    )

    print("")
    print("=" * 60)
    print(" PHASE 2 BASELINE ML COMPLETE")
    print("=" * 60)
    print("")
    print("[PASS] Feature engineering")
    print("[PASS] Chronological dataset split")
    print("[PASS] Logistic Regression")
    print("[PASS] XGBoost")
    print("[PASS] Test-set evaluation")
    print("[PASS] Model artifacts")
    print("[PASS] Prediction reports")
    print("")
    print(
        "IMPORTANT: The displayed metrics are actual measured "
        "results from this development dataset."
    )


if __name__ == "__main__":
    main()
