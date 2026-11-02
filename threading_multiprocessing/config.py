"""Runtime settings for one pipeline run.

Loads optional overrides from ``.env`` beside this package, resolves paths
relative to the project directory, and exposes tickers, timestamp file paths,
the CSV destination, and thread-pool size.
"""

from models import StockTicker
from typing import List, Dict
import os
from logging import getLogger
from pathlib import Path
from dotenv import load_dotenv
from constants import (
    DATA_DIR,
    DEFAULT_DESTINATION_FILE_PATH,
    DEFAULT_MAX_WORKERS,
    ENV_DESTINATION_FILE_PATH,
    ENV_MAX_WORKERS,
    MIN_WORKERS,
    TIMESTAMP_FILE_SUFFIX,
)
from errors import ConfigError

PROJECT_ROOT = Path(__file__).resolve().parent


def resolve_project_path(path: str) -> str:
    """Turn a project-relative path into an absolute path under ``PROJECT_ROOT``.

    Absolute paths are returned unchanged.
    """
    candidate = Path(path)
    if candidate.is_absolute():
        return str(candidate)
    return str(PROJECT_ROOT / candidate)

logger = getLogger(__name__)


class Config:
    """Immutable view of paths and concurrency limits for one pipeline run."""

    def __init__(
        self,
        stock_tickers: List[StockTicker],
        timestamps_file_path_dict: Dict[StockTicker, str],
        destination_file_path: str,
        max_workers: int,
    ):
        """Store tickers, absolute timestamp file paths, report path, and worker count."""
        self._stock_tickers = stock_tickers
        self._timestamps_file_path_dict = timestamps_file_path_dict
        self._destination_file_path = destination_file_path
        self._max_workers = max_workers

    @classmethod
    def from_env(cls) -> "Config":
        """Build config from ``constants`` defaults and environment variables.

        Tickers come from ``StockTicker`` (enum definition order). Timestamp files are
        ``data/{TICKER}.txt`` under the project directory. ``DESTINATION_FILE_PATH``
        and ``MAX_WORKERS`` override ``DEFAULT_DESTINATION_FILE_PATH`` and
        ``DEFAULT_MAX_WORKERS`` when set.

        Raises:
            ConfigError: When ``MAX_WORKERS`` is not an integer or is below
                ``MIN_WORKERS``.
        """
        load_dotenv(PROJECT_ROOT / ".env")
        stock_tickers = list(StockTicker)
        timestamps_file_path_dict = {
            ticker: str(PROJECT_ROOT / DATA_DIR / f"{ticker.value}{TIMESTAMP_FILE_SUFFIX}")
            for ticker in stock_tickers
        }
        destination_raw = os.getenv(ENV_DESTINATION_FILE_PATH, DEFAULT_DESTINATION_FILE_PATH)
        destination_file_path = resolve_project_path(destination_raw)
        max_workers_raw = os.getenv(ENV_MAX_WORKERS, str(DEFAULT_MAX_WORKERS))
        try:
            max_workers = int(max_workers_raw)
        except ValueError as exc:
            raise ConfigError(
                f"{ENV_MAX_WORKERS} must be an integer, got {max_workers_raw!r}"
            ) from exc
        if max_workers < MIN_WORKERS:
            raise ConfigError(
                f"{ENV_MAX_WORKERS} must be at least {MIN_WORKERS}, got {max_workers}"
            )
        config = cls(
            stock_tickers=stock_tickers,
            timestamps_file_path_dict=timestamps_file_path_dict,
            destination_file_path=destination_file_path,
            max_workers=max_workers,
        )
        logger.info(
            "Config loaded: tickers=%s destination=%s max_workers=%d",
            [ticker.value for ticker in stock_tickers],
            destination_file_path,
            max_workers,
        )
        return config
    @property
    def stock_tickers(self) -> list[StockTicker]:
        """Tickers to fetch and include in the report."""
        return self._stock_tickers

    @property
    def timestamps_file_path_dict(self) -> dict[StockTicker, str]:
        """Absolute path to each ticker's required-minute timestamp file."""
        return self._timestamps_file_path_dict

    @property
    def destination_file_path(self) -> str:
        """Absolute path where ``write_report`` should write the CSV."""
        return self._destination_file_path

    @property
    def max_workers(self) -> int:
        """Size of the thread pool used for Yahoo downloads."""
        return self._max_workers


