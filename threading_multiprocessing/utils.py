"""Stateless helpers with no domain orchestration or I/O."""

from datetime import datetime
from pathlib import Path

import pandas as pd

from constants import TIMESTAMP_FLOOR, TIMESTAMP_FORMAT

PROJECT_ROOT = Path(__file__).resolve().parent


def resolve_project_path(path: str) -> str:
    """Turn a project-relative path into an absolute path under ``PROJECT_ROOT``.

    Absolute paths are returned unchanged.
    """
    candidate = Path(path)
    if candidate.is_absolute():
        return str(candidate)
    return str(PROJECT_ROOT / candidate)


def format_timestamp(timestamp: str) -> datetime:
    """Parse one line as ``YYYY-MM-DD HH:MM:SS.ffffff``.

    Raises ``ValueError`` when the line does not match that format.
    """
    return datetime.strptime(timestamp, TIMESTAMP_FORMAT)


def strip_seconds_and_microseconds(timestamps: pd.Series) -> pd.Series:
    """Floor each value to the start of its minute (``TIMESTAMP_FLOOR``)."""
    ts = pd.to_datetime(timestamps)
    return ts.dt.floor(TIMESTAMP_FLOOR)


def minute_price_change_pct(ohlcv: pd.DataFrame) -> pd.Series:
    """Compute ``(Close - Open) / Open * 100`` for each row in ``ohlcv``."""
    open_price = ohlcv["Open"]
    return (ohlcv["Close"] - open_price) / open_price * 100
