"""
SentinelX Behavioral Signal Adapter
"""

from pathlib import Path
import pandas as pd



class BehavioralSignalAdapter:


    def __init__(self, root):

        self.root = Path(root)



    def generate_signals(self):


        input_path = (
            self.root /
            "reports" /
            "behavior" /
            "behavioral_risk.parquet"
        )


        output_path = (
            self.root /
            "reports" /
            "behavior" /
            "behavioral_signals.parquet"
        )


        df = pd.read_parquet(input_path)



        if "transaction_id" not in df.columns:

            raise ValueError(
                "transaction_id missing"
            )


        result = pd.DataFrame()


        result["transaction_id"] = (
            df["transaction_id"]
        )


        # Phase 3 actual column

        result["behavioral_risk"] = (

            pd.to_numeric(

                df["behavioral_risk_score"],

                errors="coerce"

            )

            .fillna(0)

            .clip(0,100)

        )



        # Additional signals

        for column in [

            "velocity_score",

            "merchant_risk_score",

            "device_activity_score"

        ]:


            if column in df.columns:

                result[column] = df[column]



        result["risk_signals"] = (

            df["risk_signals"]

            if "risk_signals" in df.columns

            else ""

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
