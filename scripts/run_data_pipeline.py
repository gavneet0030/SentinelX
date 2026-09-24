from __future__ import annotations

from sentinelx.data.ingestion.loader import (
    load_transactions,
)

from sentinelx.data.processing.clean import (
    clean_transactions,
)

from sentinelx.data.processing.storage import (
    save_parquet,
)

from sentinelx.data.validation.transaction_validator import (
    validate_transactions,
)


def run_pipeline() -> None:

    input_path = (
        "data/raw/transactions.csv"
    )

    output_path = (
        "data/processed/transactions.parquet"
    )

    print(
        "Loading transactions..."
    )

    df = load_transactions(
        input_path
    )

    print(
        f"Loaded: {len(df):,}"
    )

    print(
        "Validating raw data..."
    )

    validate_transactions(df)

    print(
        "Cleaning transactions..."
    )

    cleaned = clean_transactions(
        df
    )

    print(
        f"After cleaning: "
        f"{len(cleaned):,}"
    )

    print(
        "Validating cleaned data..."
    )

    validate_transactions(
        cleaned
    )

    print(
        "Writing Parquet..."
    )

    output = save_parquet(
        cleaned,
        output_path,
    )

    print()
    print(
        "=================================================="
    )
    print(
        " DATA PIPELINE COMPLETE"
    )
    print(
        "=================================================="
    )
    print(
        f"Input : {input_path}"
    )
    print(
        f"Output: {output}"
    )
    print(
        f"Rows  : {len(cleaned):,}"
    )


if __name__ == "__main__":
    run_pipeline()
