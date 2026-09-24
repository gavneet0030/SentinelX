from pathlib import Path

import pandas as pd


def calibrate_graph_score(df):

    score = (

        df["shared_device"] * 25

        +

        df["shared_merchant"] * 15

        +

        df["new_device"] * 8

        +

        df["new_merchant"] * 5

        +

        df["device_customer_degree"]
        .clip(0,5) * 4

        +

        df["merchant_customer_degree"]
        .clip(0,5) * 2

    )


    df["graph_risk_score"] = (
        score.clip(0,100)
    )


    return df



path = Path(
    "reports/graph/graph_features.parquet"
)


df = pd.read_parquet(path)


df = calibrate_graph_score(df)


df.to_parquet(
    path,
    index=False
)


print()
print("Graph calibration complete")
print()

print(
    df["graph_risk_score"]
    .describe()
    .to_string()
)

print()

print(
    "Unique scores:",
    df["graph_risk_score"].nunique()
)

