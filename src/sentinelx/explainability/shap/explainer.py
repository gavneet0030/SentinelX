from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap


class SHAPExplainer:

    def __init__(self, model_path: str):

        self.model_path = Path(model_path)
        self.pipeline = joblib.load(self.model_path)

    def explain(self, df: pd.DataFrame) -> pd.DataFrame:

        model = self.pipeline

        if not hasattr(model, "named_steps"):
            raise ValueError(
                "Expected a sklearn Pipeline."
            )

        preprocessing = model[:-1]
        estimator = model[-1]

        X_transformed = preprocessing.transform(df)

        explainer = shap.Explainer(
            estimator,
            X_transformed,
        )

        shap_values = explainer(
            X_transformed
        )

        values = shap_values.values

        if values.ndim == 3:
            values = values[:, :, 1]

        feature_names = list(
            getattr(
                preprocessing,
                "get_feature_names_out",
                lambda: [
                    f"feature_{i}"
                    for i in range(values.shape[1])
                ],
            )()
        )

        output = pd.DataFrame(
            values,
            columns=feature_names,
            index=df.index,
        )

        return output


def top_shap_reasons(
    shap_df: pd.DataFrame,
    top_n: int = 5,
):

    reasons = []

    for idx, row in shap_df.iterrows():

        ranked = (
            row.abs()
            .sort_values(
                ascending=False
            )
            .head(top_n)
        )

        transaction_reasons = []

        for feature in ranked.index:

            value = row[feature]

            direction = (
                "increases"
                if value > 0
                else "decreases"
            )

            transaction_reasons.append(
                f"{feature}: {direction} fraud risk"
            )

        reasons.append(
            transaction_reasons
        )

    return reasons
