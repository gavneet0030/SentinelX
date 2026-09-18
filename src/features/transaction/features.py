"""
Transaction feature engineering.
"""

import numpy as np
import pandas as pd


def add_transaction_features(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    df = dataframe.copy()

    if "amount" in df.columns:
        df["log_amount"] = np.log1p(
            df["amount"].clip(lower=0)
        )

    return df
