import pandas as pd

from sentinelx.risk.fusion.risk_context import (
    prepare_risk_context
)



def test_signal_strength():


    df=pd.DataFrame({

        "fraud_probability":[0.8],

        "behavioral_risk":[50],

        "anomaly_score":[0.9]

    })


    result=prepare_risk_context(df)


    assert (
        result["signal_strength"]
        .iloc[0]
        >0
    )



def test_missing_columns_safe():


    df=pd.DataFrame({

        "transaction_id":[1]

    })


    result=prepare_risk_context(df)


    assert (
        "signal_strength"
        in result.columns
    )
