from sentinelx.state.redis_store import RedisStateStore


def test_hot_state():

    store = RedisStateStore()

    assert store.ping() is True

    transaction_key = (
        "sentinelx:transaction:test_1001"
    )

    velocity_key = (
        "sentinelx:velocity:"
        "customer:test_1001:1m"
    )

    store.set_json(
        transaction_key,
        {
            "event_id": "test_1001",
            "risk_score": 72.5,
            "decision": "REVIEW",
        },
        ttl_seconds=300,
    )

    transaction = store.get_json(
        transaction_key
    )

    assert transaction is not None
    assert transaction["event_id"] == "test_1001"
    assert transaction["risk_score"] == 72.5
    assert transaction["decision"] == "REVIEW"

    store.delete(velocity_key)

    count_1 = store.increment(
        velocity_key,
        ttl_seconds=60,
    )

    count_2 = store.increment(
        velocity_key,
    )

    count_3 = store.increment(
        velocity_key,
    )

    assert count_1 == 1
    assert count_2 == 2
    assert count_3 == 3

    store.delete(transaction_key)
    store.delete(velocity_key)

    store.close()
