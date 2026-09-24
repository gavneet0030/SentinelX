"""
SentinelX Phase 5.1 Feature Fusion Pipeline.
"""


from pathlib import Path
import pandas as pd


from sentinelx.risk.fusion.signal_loader import (
    SignalLoader
)


from sentinelx.risk.fusion.risk_context import (
    prepare_risk_context
)



ROOT=Path(__file__).resolve().parents[2]


OUTPUT=(

ROOT/
"reports"/
"risk"/
"fusion"

)



def run():


    OUTPUT.mkdir(
        parents=True,
        exist_ok=True
    )


    print("="*60)
    print("SENTINELX RISK FEATURE FUSION")
    print("="*60)



    loader=SignalLoader(ROOT)



    print()
    print("Loading signals...")



    merged=loader.merge_all_signals()



    print(
        "Merged rows:",
        len(merged)
    )



    print()
    print("Preparing risk context...")



    context=prepare_risk_context(
        merged
    )



    context.to_parquet(

        OUTPUT/
        "risk_context.parquet",

        index=False

    )


    context.to_csv(

        OUTPUT/
        "risk_context.csv",

        index=False

    )



    print()
    print(
        context[
            [
                "fraud_probability",
                "behavioral_risk",
                "anomaly_score",
                "signal_strength"
            ]
        ]
        .describe()
    )


    print()
    print("="*60)
    print("RISK FUSION COMPLETE")
    print("="*60)



if __name__=="__main__":

    run()
