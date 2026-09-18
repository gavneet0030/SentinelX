"""
Explainability utilities.

Explanations must be derived from actual evidence.
"""


def build_rule_explanation(
    signals: list[str],
) -> list[str]:

    return list(dict.fromkeys(signals))
