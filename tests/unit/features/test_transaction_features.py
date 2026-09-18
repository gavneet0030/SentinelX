from src.features.transaction.features import add_transaction_features


def test_log_amount_feature():

    import pandas as pd

    df = pd.DataFrame({
        "amount": [100.0, 1000.0]
    })

    result = add_transaction_features(df)

    assert "log_amount" in result.columns
