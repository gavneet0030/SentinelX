from pathlib import Path

from sentinelx.integration.ml_adapter import (
    MLSignalAdapter
)

from sentinelx.integration.behavioral_adapter import (
    BehavioralSignalAdapter
)


def test_adapters_exist():

    root = Path(".")

    assert MLSignalAdapter(root)
    assert BehavioralSignalAdapter(root)
