"""
Unified risk aggregation engine.

Combines:
- ML score
- Behavioral score
- Anomaly score
- Rule score
"""


from dataclasses import dataclass



@dataclass
class RiskOutput:

    risk_score:float
    risk_level:str
    decision:str
    signals:list



class RiskAggregator:



    def calculate(
        self,
        fraud_probability,
        behavioral_score,
        anomaly_score,
        rule_score,
        signals
    ):


        final_score=(

            fraud_probability * 40

            +

            behavioral_score/100 * 25

            +

            anomaly_score * 20

            +

            rule_score/100 * 15

        )


        final_score=min(
            round(final_score,2),
            100
        )


        if final_score >= 85:

            level="CRITICAL"
            decision="BLOCK"


        elif final_score >= 60:

            level="HIGH"
            decision="REVIEW"


        elif final_score >= 30:

            level="MEDIUM"
            decision="REVIEW"


        else:

            level="LOW"
            decision="APPROVE"



        return RiskOutput(

            risk_score=final_score,

            risk_level=level,

            decision=decision,

            signals=signals

        )
