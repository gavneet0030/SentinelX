from sentinelx.state.redis_store import RedisStateStore


def test_redis_state_store():

    store = RedisStateStore()

    assert store.ping() is True

    store.set_json(
        "sentinelx:test",
        {
            "event_id": "test_001",
            "risk_score": 42.5,
        },
        ttl_seconds=60,
    )

    value = store.get_json(
        "sentinelx:test"
    )

    assert value is not None
    assert value["event_id"] == "test_001"
    assert value["risk_score"] == 42.5

    store.delete(
        "sentinelx:test"
    )

    store.close()
