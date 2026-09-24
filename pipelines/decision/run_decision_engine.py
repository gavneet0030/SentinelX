from pathlib import Path

import pandas as pd

from sentinelx.decision.engine import (
    DecisionEngine,
    DecisionPolicy,
)

from sentinelx.alerts.alert_engine import (
    AlertEngine,
)


ROOT = Path(__file__).resolve().parents[2]


INPUT = (
    ROOT
    /
    "reports"
    /
    "risk"
    /
    "fusion"
    /
    "graph_risk_context.parquet"
)


EXPLANATION_INPUT = (
    ROOT
    /
    "reports"
    /
    "explainability"
    /
    "risk_explanations.parquet"
)


DECISION_OUTPUT = (
    ROOT
    /
    "reports"
    /
    "decisions"
    /
    "decision_records.parquet"
)


ALERT_OUTPUT = (
    ROOT
    /
    "reports"
    /
    "alerts"
    /
    "alerts.parquet"
)



def main():

    print("=" * 60)
    print("SENTINELX DECISION ENGINE")
    print("=" * 60)


    risk = pd.read_parquet(
        INPUT
    )


    explanations = pd.read_parquet(
        EXPLANATION_INPUT
    )


    explanation_columns = [
        "transaction_id",
        "reasons",
    ]


    explanations = explanations[
        explanation_columns
    ]


    df = risk.merge(
        explanations,
        on="transaction_id",
        how="left",
    )


    policy = DecisionPolicy()

    decision_engine = DecisionEngine(
        policy
    )

    alert_engine = AlertEngine()


    decisions = []

    alerts = []


    for row in df.itertuples(
        index=False
    ):

        decision = (
            decision_engine.evaluate(
                transaction_id=
                    row.transaction_id,

                risk_score=
                    row.final_risk_score,
            )
        )


        alert = (
            alert_engine.create_alert(
                transaction_id=
                    row.transaction_id,

                risk_score=
                    row.final_risk_score,

                decision=
                    decision["decision"],

                severity=
                    decision["severity"],

                explanation=
                    row.reasons
                    if isinstance(
                        row.reasons,
                        str
                    )
                    else "",
            )
        )


        decisions.append(
            decision
        )

        alerts.append(
            alert
        )


    decision_df = pd.DataFrame(
        decisions
    )

    alert_df = pd.DataFrame(
        alerts
    )


    DECISION_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    ALERT_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    decision_df.to_parquet(
        DECISION_OUTPUT,
        index=False,
    )

    alert_df.to_parquet(
        ALERT_OUTPUT,
        index=False,
    )


    print()
    print("Transactions:", len(df))

    print()
    print("Decision distribution:")
    print(
        decision_df[
            "decision"
        ].value_counts()
    )

    print()
    print("Severity distribution:")
    print(
        decision_df[
            "severity"
        ].value_counts()
    )

    print()
    print(
        "Alerts created:",
        int(
            alert_df[
                "alert_created"
            ].sum()
        ),
    )

    print()
    print(
        "DECISION ENGINE COMPLETE"
    )


if __name__ == "__main__":

    main()
