from pathlib import Path

import pandas as pd

from sentinelx.graph.network.builder import build_graph_edges
from sentinelx.graph.features.graph_features import build_graph_features


ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "data" / "processed" / "transactions.parquet"

EDGE_OUTPUT = ROOT / "reports" / "graph" / "transaction_graph_edges.parquet"

FEATURE_OUTPUT = ROOT / "reports" / "graph" / "graph_features.parquet"


def main():

    print("Loading transactions...")

    df = pd.read_parquet(INPUT)

    print(f"Transactions: {len(df):,}")

    edges = build_graph_edges(df)

    EDGE_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    edges.to_parquet(
        EDGE_OUTPUT,
        index=False,
    )

    print(f"Graph edges: {len(edges):,}")

    features = build_graph_features(df)

    features.to_parquet(
        FEATURE_OUTPUT,
        index=False,
    )

    print(f"Graph feature rows: {len(features):,}")

    print()
    print("Graph risk summary:")
    print(
        features["graph_risk_score"]
        .describe()
        .to_string()
    )

    print()
    print("GRAPH ENGINE COMPLETE")


if __name__ == "__main__":
    main()
