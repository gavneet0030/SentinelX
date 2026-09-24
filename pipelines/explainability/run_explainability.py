from pathlib import Path
import json

import pandas as pd

from sentinelx.explainability.evidence.evidence_engine import (
    build_explanation
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


OUTPUT = (
    ROOT
    /
    "reports"
    /
    "explainability"
    /
    "risk_explanations.parquet"
)


SUMMARY = (
    ROOT
    /
    "reports"
    /
    "explainability"
    /
    "explanation_summary.json"
)



def main():


    print("="*60)
    print("SENTINELX EXPLAINABILITY ENGINE")
    print("="*60)


    df = pd.read_parquet(INPUT)


    explanations=[]


    for _,row in df.iterrows():


        result = build_explanation(row)


        explanations.append(

            {
                "transaction_id":
                    row["transaction_id"],

                "risk_score":
                    result["risk_score"],

                "risk_level":
                    result["risk_level"],

                "reason_count":
                    len(result["reasons"]),

                "reasons":
                    " | ".join(result["reasons"]),

                "evidence":
                    json.dumps(
                        result["evidence"]
                    )
            }

        )



    output=pd.DataFrame(
        explanations
    )


    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    output.to_parquet(
        OUTPUT,
        index=False
    )



    summary={

        "transactions":
            len(output),

        "with_evidence":
            int(
                (output.reason_count > 0)
                .sum()
            ),

        "high_risk":
            int(
                (
                    output.risk_level
                    .isin(
                        [
                            "HIGH",
                            "CRITICAL"
                        ]
                    )
                )
                .sum()
            )

    }


    SUMMARY.write_text(
        json.dumps(
            summary,
            indent=2
        ),
        encoding="utf-8"
    )


    print()

    print(
        "Transactions:",
        len(output)
    )

    print(
        "Evidence generated:",
        summary["with_evidence"]
    )

    print(
        "High risk:",
        summary["high_risk"]
    )


    print()

    print(
        "EXPLAINABILITY COMPLETE"
    )



if __name__=="__main__":

    main()

