"""
SentinelX Phase 5.2 integration pipeline.
"""

from pathlib import Path

from sentinelx.integration.ml_adapter import (
    MLSignalAdapter
)

from sentinelx.integration.behavioral_adapter import (
    BehavioralSignalAdapter
)


ROOT = Path(__file__).resolve().parents[2]


def run():

    print("=" * 60)
    print("SENTINELX PHASE 5.2 SIGNAL INTEGRATION")
    print("=" * 60)

    print()
    print("[1/2] Generating ML predictions...")

    ml = MLSignalAdapter(ROOT)

    ml_output = ml.generate_predictions()

    print(
        "ML rows:",
        len(ml_output)
    )

    print(
        "Saved:",
        ROOT /
        "reports" /
        "ml" /
        "fraud_predictions.parquet"
    )

    print()
    print("[2/2] Generating behavioral signals...")

    behavioral = BehavioralSignalAdapter(ROOT)

    behavioral_output = behavioral.generate_signals()

    print(
        "Behavioral rows:",
        len(behavioral_output)
    )

    print(
        "Saved:",
        ROOT /
        "reports" /
        "behavior" /
        "behavioral_signals.parquet"
    )

    print()
    print("=" * 60)
    print("PHASE 5.2 INTEGRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run()
