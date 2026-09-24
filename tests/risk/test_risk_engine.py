from sentinelx.risk.rules.rule_engine import RuleEngine
from sentinelx.risk.aggregation.risk_aggregator import RiskAggregator



def test_rule_engine():

    engine=RuleEngine()


    result=engine.evaluate({

        "amount":10000,

        "customer_velocity_1h":10,

        "anomaly_score":0.9,

        "device_new_for_customer":1

    })


    assert len(result)>0



def test_risk_score():


    agg=RiskAggregator()


    output=agg.calculate(

        0.9,

        90,

        0.9,

        80,

        ["TEST"]

    )


    assert output.risk_score>0

    assert output.decision in [

        "BLOCK",
        "REVIEW",
        "APPROVE"

    ]
