from __future__ import annotations

import pandas as pd


def build_evidence(row):

    evidence = []


    # --------------------------------------------------------
    # ML
    # --------------------------------------------------------

    fraud_probability = float(
        row.get(
            "fraud_probability",
            0,
        )
    )

    if fraud_probability >= 0.10:

        evidence.append(
            {
                "source": "ML",
                "severity": "HIGH",
                "reason": (
                    "Fraud model probability is elevated."
                ),
                "value": fraud_probability,
            }
        )

    elif fraud_probability >= 0.05:

        evidence.append(
            {
                "source": "ML",
                "severity": "MEDIUM",
                "reason": (
                    "Fraud model probability is above baseline."
                ),
                "value": fraud_probability,
            }
        )


    # --------------------------------------------------------
    # BEHAVIOR
    # --------------------------------------------------------

    behavioral = float(
        row.get(
            "behavioral_risk",
            0,
        )
    )

    if behavioral >= 45:

        evidence.append(
            {
                "source": "BEHAVIOR",
                "severity": "HIGH",
                "reason": (
                    "Customer behavior differs materially "
                    "from historical patterns."
                ),
                "value": behavioral,
            }
        )

    elif behavioral >= 30:

        evidence.append(
            {
                "source": "BEHAVIOR",
                "severity": "MEDIUM",
                "reason": (
                    "Behavioral risk is elevated."
                ),
                "value": behavioral,
            }
        )


    # --------------------------------------------------------
    # ANOMALY
    # --------------------------------------------------------

    anomaly = float(
        row.get(
            "anomaly_score",
            0,
        )
    )

    if anomaly >= 0.90:

        evidence.append(
            {
                "source": "ANOMALY",
                "severity": "HIGH",
                "reason": (
                    "Transaction is highly anomalous "
                    "relative to learned patterns."
                ),
                "value": anomaly,
            }
        )

    elif anomaly >= 0.70:

        evidence.append(
            {
                "source": "ANOMALY",
                "severity": "MEDIUM",
                "reason": (
                    "Transaction shows anomalous behavior."
                ),
                "value": anomaly,
            }
        )


    # --------------------------------------------------------
    # GRAPH
    # --------------------------------------------------------

    graph = float(
        row.get(
            "graph_risk_score",
            0,
        )
    )

    shared_device = int(
        row.get(
            "shared_device",
            0,
        )
    )

    shared_merchant = int(
        row.get(
            "shared_merchant",
            0,
        )
    )

    if graph >= 70:

        evidence.append(
            {
                "source": "GRAPH",
                "severity": "HIGH",
                "reason": (
                    "Transaction is associated with "
                    "high graph-network risk."
                ),
                "value": graph,
            }
        )

    elif graph >= 50:

        evidence.append(
            {
                "source": "GRAPH",
                "severity": "MEDIUM",
                "reason": (
                    "Graph relationships indicate "
                    "elevated network risk."
                ),
                "value": graph,
            }
        )


    if shared_device:

        evidence.append(
            {
                "source": "GRAPH",
                "severity": "MEDIUM",
                "reason": (
                    "Device is associated with multiple "
                    "customers."
                ),
                "value": 1,
            }
        )


    if shared_merchant:

        evidence.append(
            {
                "source": "GRAPH",
                "severity": "LOW",
                "reason": (
                    "Merchant is associated with "
                    "multiple customers."
                ),
                "value": 1,
            }
        )


    return evidence


def build_explanation(row):

    evidence = build_evidence(row)

    evidence = sorted(
        evidence,
        key=lambda x: {
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1,
        }.get(
            x["severity"],
            0,
        ),
        reverse=True,
    )

    reasons = [
        item["reason"]
        for item in evidence
    ]

    return {
        "risk_score": float(
            row.get(
                "final_risk_score",
                0,
            )
        ),
        "risk_level": str(
            row.get(
                "final_risk_level",
                "UNKNOWN",
            )
        ),
        "reasons": reasons,
        "evidence": evidence,
    }
