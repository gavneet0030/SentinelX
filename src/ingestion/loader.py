"""
Data ingestion interfaces.
"""

from pathlib import Path
import pandas as pd


def load_csv(path: str | Path) -> pd.DataFrame:
    """
    Load a CSV dataset into a pandas DataFrame.
    """
    return pd.read_csv(path)
