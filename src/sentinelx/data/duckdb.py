from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


def transaction_summary(
    parquet_path: str | Path,
) -> pd.DataFrame:

    parquet_path = Path(
        parquet_path
    )

    if not parquet_path.exists():
        raise FileNotFoundError(
            f"Parquet not found: {parquet_path}"
        )

    connection = duckdb.connect()

    try:

        query = """
        SELECT
            COUNT(*) AS transaction_count,
            COUNT(
                DISTINCT customer_id
            ) AS customer_count,
            COUNT(
                DISTINCT merchant_id
            ) AS merchant_count,
            ROUND(
                SUM(amount),
                2
            ) AS total_amount,
            ROUND(
                AVG(amount),
                2
            ) AS average_amount,
            SUM(
                CASE
                    WHEN is_fraud = TRUE
                    THEN 1
                    ELSE 0
                END
            ) AS fraud_count
        FROM read_parquet(?)
        """

        return connection.execute(
            query,
            [str(parquet_path)],
        ).df()

    finally:
        connection.close()
