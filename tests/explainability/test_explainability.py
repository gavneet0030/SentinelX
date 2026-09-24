import pandas as pd

from sentinelx.explainability.evidence.evidence_engine import (
    build_evidence,
    build_explanation,
)


def make_row():

    return pd.Series(
        {
            "transaction_id": "tx-001",
            "fraud_probability": 0.12,
            "behavioral_risk": 50.0,
            "anomaly_score": 0.95,
            "graph_risk_score": 80.0,
            "shared_device": 1,
            "shared_merchant": 1,
            "final_risk_score": 90.0,
            "final_risk_level": "CRITICAL",
        }
    )


def test_evidence_generation():

    evidence = build_evidence(
        make_row()
    )

    assert len(evidence) > 0

    sources = {
        item["source"]
        for item in evidence
    }

    assert "ML" in sources
    assert "BEHAVIOR" in sources
    assert "ANOMALY" in sources
    assert "GRAPH" in sources


def test_explanation_structure():

    explanation = build_explanation(
        make_row()
    )

    assert "risk_score" in explanation
    assert "risk_level" in explanation
    assert "reasons" in explanation
    assert "evidence" in explanation

    assert explanation["risk_score"] == 90.0
    assert explanation["risk_level"] == "CRITICAL"

    assert len(
        explanation["reasons"]
    ) > 0

    assert len(
        explanation["evidence"]
    ) > 0
