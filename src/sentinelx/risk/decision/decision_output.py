"""
Decision output schema.
"""


from datetime import datetime



def create_decision_record(
    transaction_id,
    risk
):


    return {

        "transaction_id":
            transaction_id,


        "timestamp":
            datetime.utcnow().isoformat(),


        "risk_score":
            risk.risk_score,


        "risk_level":
            risk.risk_level,


        "decision":
            risk.decision,


        "risk_signals":
            risk.signals

    }
