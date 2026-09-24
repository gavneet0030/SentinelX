from pathlib import Path

from sentinelx.risk.fusion.graph_fusion import (
    GraphRiskFusion
)


ROOT=Path(__file__).resolve().parents[2]


def main():

    print("="*60)

    print(
        "SENTINELX GRAPH ENHANCED RISK FUSION"
    )

    print("="*60)


    engine=GraphRiskFusion(ROOT)


    result=engine.run()


    print()

    print(
        "Rows:",
        len(result)
    )


    print()

    print(
        result[
            [
                "fraud_probability",
                "behavioral_risk",
                "anomaly_score",
                "graph_risk_score",
                "final_risk_score"
            ]
        ]
        .describe()
    )


    print()

    print(
        result["final_risk_level"]
        .value_counts()
    )


    print()

    print(
        "GRAPH FUSION COMPLETE"
    )


if __name__=="__main__":

    main()
