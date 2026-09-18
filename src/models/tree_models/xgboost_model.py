"""
Tree-based model factory.
"""

from xgboost import XGBClassifier


def create_xgboost_model() -> XGBClassifier:

    return XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42,
    )
