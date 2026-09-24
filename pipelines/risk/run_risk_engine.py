"""
SentinelX Phase 5 unified risk pipeline.
"""


from pathlib import Path
import pandas as pd

from sentinelx.risk.rules.rule_engine import RuleEngine
from sentinelx.risk.aggregation.risk_aggregator import RiskAggregator
from sentinelx.risk.decision.decision_output import (
    create_decision_record
)


ROOT=Path(__file__).resolve().parents[2]


INPUT=ROOT/"reports"/"anomaly"/"anomaly_scores.parquet"

OUTPUT_DIR=ROOT/"reports"/"risk"



def run():


    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    print("="*60)
    print("SENTINELX UNIFIED RISK ENGINE")
    print("="*60)



    df=pd.read_parquet(INPUT)



    rule_engine=RuleEngine()

    aggregator=RiskAggregator()



    results=[]


    for _,row in df.iterrows():


        rules=rule_engine.evaluate(
            row.to_dict()
        )


        rule_score=(
            rule_engine
            .calculate_rule_score(rules)
        )


        fraud_probability=float(
            row.get(
                "fraud_probability",
                0
            )
        )


        behavioral=float(
            row.get(
                "behavioral_risk",
                0
            )
        )


        anomaly=float(
            row.get(
                "anomaly_score",
                0
            )
        )



        signals=[

            r.signal

            for r in rules

        ]



        risk=aggregator.calculate(

            fraud_probability,

            behavioral,

            anomaly,

            rule_score,

            signals

        )



        results.append(

            create_decision_record(

                row["transaction_id"],

                risk

            )

        )



    output=pd.DataFrame(results)



    output.to_parquet(

        OUTPUT_DIR/
        "risk_decisions.parquet",

        index=False

    )


    output.to_csv(

        OUTPUT_DIR/
        "risk_decisions.csv",

        index=False

    )


    print()

    print(
        output["risk_level"]
        .value_counts()
    )


    print()

    print("="*60)

    print("RISK ENGINE COMPLETE")

    print("="*60)



if __name__=="__main__":

    run()
