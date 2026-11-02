"""Parse per-ticker timestamp text files into minute-floored ``datetime`` series.

Each line is one required report minute. Seconds and microseconds are stripped
so they align with Yahoo 1m bar indices.
"""

import pandas as pd
import os
from datetime import datetime
from logging import getLogger
from constants import TIMESTAMP_FLOOR, TIMESTAMP_FORMAT

logger = getLogger(__name__)


def format_timestamp(timestamp: str) -> datetime:
    """Parse one line as ``YYYY-MM-DD HH:MM:SS.ffffff``.

    Raises ``ValueError`` when the line does not match that format.
    """
    return datetime.strptime(timestamp, TIMESTAMP_FORMAT)

def strip_seconds_and_microseconds(timestamps: pd.Series) -> pd.Series:
    """Floor each value to the start of its minute (``TIMESTAMP_FLOOR``)."""
    ts = pd.to_datetime(timestamps)
    return ts.dt.floor(TIMESTAMP_FLOOR)


def read_timestamps_from_txt(file_path: str) -> pd.Series:
    """Read and normalize required minutes from a whitespace-stripped line file.

    Args:
        file_path: Path to a ``.txt`` file with one ``TIMESTAMP_FORMAT`` line each.

    Returns:
        Series of timezone-naive datetimes floored to the minute.

    Raises:
        FileNotFoundError: When ``file_path`` does not exist.
        ValueError: When the file is empty or any line fails ``format_timestamp``.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    with open(file_path, "r", encoding="utf-8") as file:
        formatted_timestamps = pd.Series([format_timestamp(line.strip()) for line in file.readlines()])
    if formatted_timestamps.empty:
        raise ValueError(f"No timestamps in {file_path}")
    timestamps = strip_seconds_and_microseconds(formatted_timestamps)
    logger.debug(
        f"Parsed {len(timestamps)} timestamps from {file_path} "
        f"({timestamps.min()} to {timestamps.max()})"
    )
    return timestamps
