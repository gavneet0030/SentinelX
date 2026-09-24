"""
SentinelX deterministic fraud risk rules.

Rules are explainable and auditable.
"""


from dataclasses import dataclass
from typing import List


@dataclass
class RuleResult:

    triggered: bool
    score: int
    signal: str
    description: str



class RuleEngine:


    def evaluate(self,row)->List[RuleResult]:

        results=[]


        amount=float(
            row.get(
                "amount",
                0
            )
        )


        velocity=float(
            row.get(
                "customer_velocity_1h",
                0
            )
        )


        anomaly=float(
            row.get(
                "anomaly_score",
                0
            )
        )


        new_device=int(
            row.get(
                "device_new_for_customer",
                0
            )
        )


        #
        # Rule 1
        #

        if amount > 5000:

            results.append(
                RuleResult(
                    True,
                    20,
                    "HIGH_AMOUNT",
                    "Transaction amount exceeds threshold"
                )
            )


        #
        # Rule 2
        #

        if velocity >= 5:

            results.append(
                RuleResult(
                    True,
                    20,
                    "HIGH_VELOCITY",
                    "Customer transaction velocity is abnormal"
                )
            )


        #
        # Rule 3
        #

        if new_device == 1:

            results.append(
                RuleResult(
                    True,
                    15,
                    "NEW_DEVICE",
                    "Transaction originated from new device"
                )
            )


        #
        # Rule 4
        #

        if anomaly >= 0.7:

            results.append(
                RuleResult(
                    True,
                    25,
                    "ANOMALY_SIGNAL",
                    "Transaction behaviour is anomalous"
                )
            )


        return results



    def calculate_rule_score(
        self,
        results
    ):

        return min(
            sum(
                r.score
                for r in results
            ),
            100
        )
