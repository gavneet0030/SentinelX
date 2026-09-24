from __future__ import annotations

import pandas as pd


def build_graph_edges(df: pd.DataFrame) -> pd.DataFrame:
    required = {
        "transaction_id",
        "customer_id",
        "merchant_id",
        "device_id",
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    rows = []

    for row in df.itertuples(index=False):
        rows.append(
            {
                "transaction_id": row.transaction_id,
                "source_type": "customer",
                "source_id": str(row.customer_id),
                "target_type": "device",
                "target_id": str(row.device_id),
                "relationship": "USES_DEVICE",
            }
        )

        rows.append(
            {
                "transaction_id": row.transaction_id,
                "source_type": "customer",
                "source_id": str(row.customer_id),
                "target_type": "merchant",
                "target_id": str(row.merchant_id),
                "relationship": "VISITS_MERCHANT",
            }
        )

    return pd.DataFrame(rows)


def save_graph_edges(
    df: pd.DataFrame,
    output_path: str,
) -> pd.DataFrame:

    edges = build_graph_edges(df)

    output = output_path
    edges.to_parquet(output, index=False)

    return edges
