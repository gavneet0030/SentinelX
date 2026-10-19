
from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .dataset import time_based_split
from .evaluate import evaluate_model
from .features import CATEGORICAL_FEATURES, TARGET_COLUMN, build_features
from .threshold import optimize_threshold
from sentinelx.graph.features.graph_features import build_graph_features


TRANSACTION_FEATURES = ["amount", "log_amount"]
TEMPORAL_FEATURES = ["hour", "day_of_week", "is_weekend"]
BEHAVIORAL_FEATURES = [
    "customer_txn_count_prior",
    "customer_avg_amount_prior",
    "merchant_txn_count_prior",
    "device_txn_count_prior",
]
GRAPH_FEATURES = [
    "customer_device_degree",
    "customer_merchant_degree",
    "device_customer_degree",
    "merchant_customer_degree",
    "shared_device",
    "shared_merchant",
    "new_device",
    "new_merchant",
    "graph_risk_score",
]

EXPERIMENTS = {
    "transaction_baseline": TRANSACTION_FEATURES + CATEGORICAL_FEATURES,
    "transaction_temporal": (
        TRANSACTION_FEATURES + TEMPORAL_FEATURES + CATEGORICAL_FEATURES
    ),
    "transaction_behavioral": (
        TRANSACTION_FEATURES + BEHAVIORAL_FEATURES + CATEGORICAL_FEATURES
    ),
    "full_with_graph": (
        TRANSACTION_FEATURES
        + TEMPORAL_FEATURES
        + BEHAVIORAL_FEATURES
        + GRAPH_FEATURES
        + CATEGORICAL_FEATURES
    ),
}

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "merchant_id",
    "timestamp",
    "amount",
    "payment_method",
    "channel",
    "country",
    "device_id",
    "is_fraud",
]


def make_model(columns: list[str]) -> Pipeline:
    """Create a preprocessing and logistic-regression pipeline."""
    categorical = [c for c in columns if c in CATEGORICAL_FEATURES]
    numeric = [c for c in columns if c not in categorical]

    transformers = []

    if numeric:
        transformers.append(
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric,
            )
        )

    if categorical:
        transformers.append(
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            )
        )

    return Pipeline(
        [
            ("preprocessor", ColumnTransformer(transformers=transformers)),
            (
                "classifier",
                LogisticRegression(
                    max_iter=5000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def select_threshold(y_true, scores) -> float:
    """Select a threshold targeting at least 50% validation fraud recall."""
    result = optimize_threshold(y_true, scores, min_recall=0.50)

    if isinstance(result, dict):
        return float(result.get("threshold", 0.5))

    if isinstance(result, (int, float)):
        return float(result)

    if isinstance(result, pd.DataFrame):
        if result.empty or "threshold" not in result.columns:
            return 0.5
        return float(result.iloc[0]["threshold"])

    return 0.5


def run_feature_experiments(
    raw: pd.DataFrame,
    output_dir: str | Path = "reports/ml_experiments_scaled",
) -> pd.DataFrame:
    """Compare feature groups using chronological train/validation/test splits."""
    missing = sorted(set(REQUIRED_COLUMNS) - set(raw.columns))
    if missing:
        raise ValueError(f"Input dataset is missing required columns: {missing}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    raw = raw.copy()
    raw["timestamp"] = pd.to_datetime(
        raw["timestamp"], errors="coerce", utc=True
    )
    raw = raw.dropna(subset=["timestamp", "transaction_id", TARGET_COLUMN])
    raw = raw.sort_values(
        ["timestamp", "transaction_id"]
    ).reset_index(drop=True)

    if raw.empty:
        raise ValueError("No valid transactions remain after timestamp validation.")

    # Build transaction and historical features.
    featured = build_features(raw)

    # Keep only graph feature columns when merging. This prevents timestamp
    # and other shared columns from being renamed to timestamp_x/timestamp_y.
    graph_features = build_graph_features(raw)

    if "transaction_id" not in graph_features.columns:
        raise ValueError("Graph features must contain transaction_id.")

    available_graph_features = [
        column for column in GRAPH_FEATURES
        if column in graph_features.columns
    ]

    graph_subset = graph_features[
        ["transaction_id"] + available_graph_features
    ].copy()

    if graph_subset["transaction_id"].duplicated().any():
        raise ValueError("Graph features contain duplicate transaction_id values.")

    featured = featured.merge(
        graph_subset,
        on="transaction_id",
        how="left",
        validate="one_to_one",
    )

    if "timestamp" not in featured.columns:
        raise ValueError(
            f"Timestamp missing after feature merge. Columns: {featured.columns.tolist()}"
        )

    # Missing graph values are retained as NaN and handled by model imputation.
    train, validation, test = time_based_split(featured)

    for name, split in [
        ("training", train),
        ("validation", validation),
        ("test", test),
    ]:
        if split.empty:
            raise ValueError(f"The {name} split is empty.")
        if split[TARGET_COLUMN].nunique() < 2:
            raise ValueError(f"The {name} split must contain both target classes.")

    results = []

    for name, requested_features in EXPERIMENTS.items():
        columns = [
            column for column in requested_features
            if column in featured.columns
        ]

        if name == "full_with_graph":
            present_graph = [c for c in GRAPH_FEATURES if c in columns]
            if not present_graph:
                print("Skipping graph experiment: no graph features were produced.")
                continue
            missing_graph = [c for c in GRAPH_FEATURES if c not in columns]
            if missing_graph:
                print(f"Graph features unavailable in this run: {missing_graph}")

        if not columns:
            print(f"Skipping {name}: no usable features.")
            continue

        model = make_model(columns)
        model.fit(train[columns], train[TARGET_COLUMN].astype(int))

        validation_scores = model.predict_proba(validation[columns])[:, 1]
        validation_y = validation[TARGET_COLUMN].astype(int).to_numpy()
        threshold = select_threshold(validation_y, validation_scores)

        validation_predictions = (validation_scores >= threshold).astype(int)
        true_positives = int(((validation_y == 1) & (validation_predictions == 1)).sum())
        false_positives = int(((validation_y == 0) & (validation_predictions == 1)).sum())
        false_negatives = int(((validation_y == 1) & (validation_predictions == 0)).sum())

        validation_precision = (
            true_positives / (true_positives + false_positives)
            if true_positives + false_positives else 0.0
        )
        validation_recall = (
            true_positives / (true_positives + false_negatives)
            if true_positives + false_negatives else 0.0
        )
        validation_f1 = (
            2 * validation_precision * validation_recall
            / (validation_precision + validation_recall)
            if validation_precision + validation_recall else 0.0
        )

        started = time.perf_counter()
        metrics = evaluate_model(
            model,
            test[columns],
            test[TARGET_COLUMN].astype(int),
            model_name=name,
            output_dir=output_dir,
            threshold=threshold,
        )
        elapsed = time.perf_counter() - started

        if not isinstance(metrics, dict):
            raise TypeError("evaluate_model must return a dictionary.")

        row = dict(metrics)
        row.update(
            {
                "model": name,
                "sample_count": int(len(test)),
                "positive_count": int(test[TARGET_COLUMN].sum()),
                "threshold": threshold,
                "validation_precision": validation_precision,
                "validation_recall": validation_recall,
                "validation_f1": validation_f1,
                "validation_recall_target_met": validation_recall >= 0.50,
                "feature_count": len(columns),
                "evaluation_call_seconds": elapsed,
            }
        )
        results.append(row)

        with (output_path / f"{name}_metrics.json").open(
            "w", encoding="utf-8"
        ) as file:
            json.dump(row, file, indent=2, default=str)

        print(
            f"{name}: "
            f"PR-AUC={row.get('pr_auc', float('nan')):.4f}, "
            f"F1={row.get('f1', float('nan')):.4f}, "
            f"recall={row.get('recall', float('nan')):.4f}, "
            f"threshold={threshold:.4f}"
        )

    summary = pd.DataFrame(results)
    if summary.empty:
        raise ValueError("No experiments produced results.")

    summary.to_csv(output_path / "summary.csv", index=False)

    print(f"\nSaved experiment results to: {output_path.resolve()}")
    print(summary.to_string(index=False))
    return summary


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Compare SentinelX fraud-detection feature groups."
    )
    parser.add_argument("--data", required=True, help="Path to transaction CSV.")
    parser.add_argument(
        "--output",
        default="reports/ml_experiments_scaled",
        help="Directory for experiment results.",
    )
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    run_feature_experiments(pd.read_csv(data_path), args.output)


if __name__ == "__main__":
    main()
