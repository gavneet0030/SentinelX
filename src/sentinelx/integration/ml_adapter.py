"""
SentinelX ML Adapter
Automatic model feature compatibility layer.
"""

from pathlib import Path
import pandas as pd
import joblib



class MLSignalAdapter:


    def __init__(self,root):

        self.root=Path(root)



    def generate_predictions(self):


        data_path = (
            self.root /
            "data" /
            "processed" /
            "transactions.parquet"
        )


        model_path = (
            self.root /
            "models" /
            "baseline_xgboost" /
            "model.joblib"
        )


        output_path = (
            self.root /
            "reports" /
            "ml" /
            "fraud_predictions.parquet"
        )


        df=pd.read_parquet(
            data_path
        )


        model=joblib.load(
            model_path
        )


        pipeline=model


        print(
            "Detecting model features..."
        )


        required=[]


        try:

            preprocessor = (
                pipeline
                .named_steps
                ["preprocessor"]
            )


            required=list(
                preprocessor
                .feature_names_in_
            )


        except Exception:


            try:

                required=list(
                    pipeline
                    .feature_names_in_
                )

            except Exception:

                required=[

                    "amount"

                ]



        print(
            "Required features:",
            len(required)
        )



        X=df.copy()



        for col in required:


            if col not in X.columns:


                if col in [

                    "country",
                    "channel",
                    "payment_method"

                ]:

                    X[col]="unknown"


                else:

                    X[col]=0



        X=X[required]



        probabilities=(

            model
            .predict_proba(X)[:,1]

        )



        result=pd.DataFrame({

            "transaction_id":
            df["transaction_id"],


            "fraud_probability":
            probabilities,


            "fraud_prediction":
            (
                probabilities >= 0.5
            )
            .astype(int),


            "model_version":
            "baseline_xgboost_v1"

        })


        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        result.to_parquet(
            output_path,
            index=False
        )


        print(
            "ML predictions saved:",
            len(result)
        )


        return result
