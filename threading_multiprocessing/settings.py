"""Runtime settings for one pipeline run.

Loads optional overrides from ``.env`` beside this package, resolves paths
relative to the project directory, and exposes tickers, timestamp file paths,
the CSV destination, and thread-pool size.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from constants import (
    DATA_DIR,
    DEFAULT_DESTINATION_FILE_PATH,
    DEFAULT_MAX_WORKERS,
    MIN_WORKERS,
    PROJECT_ROOT,
    TIMESTAMP_FILE_SUFFIX,
)
from models import StockTicker
from utils import resolve_project_path


class Settings(BaseSettings):
    """Immutable view of paths and concurrency limits for one pipeline run."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    destination_file_path: str = DEFAULT_DESTINATION_FILE_PATH
    max_workers: int = Field(default=DEFAULT_MAX_WORKERS, ge=MIN_WORKERS)

    @field_validator("destination_file_path")
    @classmethod
    def _resolve_destination(cls, value: str) -> str:
        return resolve_project_path(value)

    @property
    def stock_tickers(self) -> list[StockTicker]:
        """Tickers to fetch and include in the report."""
        return list(StockTicker)

    @property
    def timestamps_file_path_dict(self) -> dict[StockTicker, str]:
        """Absolute path to each ticker's required-minute timestamp file."""
        return {
            ticker: str(PROJECT_ROOT / DATA_DIR / f"{ticker.value}{TIMESTAMP_FILE_SUFFIX}")
            for ticker in self.stock_tickers
        }
