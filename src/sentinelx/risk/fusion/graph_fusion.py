"""
SentinelX Graph Enhanced Risk Fusion
"""

from pathlib import Path

import pandas as pd



class GraphRiskFusion:


    def __init__(self,root):

        self.root=Path(root)



    def run(self):


        fusion_path = (

            self.root /
            "reports" /
            "risk" /
            "fusion" /
            "risk_context.parquet"

        )


        graph_path = (

            self.root /
            "reports" /
            "graph" /
            "graph_features.parquet"

        )


        output_path = (

            self.root /
            "reports" /
            "risk" /
            "fusion" /
            "graph_risk_context.parquet"

        )


        risk = pd.read_parquet(
            fusion_path
        )


        graph = pd.read_parquet(
            graph_path
        )


        graph_cols=[

            "transaction_id",

            "graph_risk_score",

            "shared_device",

            "shared_merchant"

        ]


        graph=graph[graph_cols]


        result=risk.merge(

            graph,

            on="transaction_id",

            how="left"

        )



        result["graph_risk_score"]=(

            pd.to_numeric(

                result["graph_risk_score"],

                errors="coerce"

            )

            .fillna(0)

        )



        result["final_risk_score"]=(

            result["signal_strength"]*70

            +

            result["graph_risk_score"]*0.30

        )



        result["final_risk_score"]=(
            result["final_risk_score"]
            .clip(0,100)
            .round(2)
        )



        result["final_risk_level"]=pd.cut(

            result["final_risk_score"],

            bins=[

                -1,
                30,
                60,
                85,
                100

            ],

            labels=[

                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL"

            ]

        )


        output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )


        result.to_parquet(

            output_path,

            index=False

        )


        return result
