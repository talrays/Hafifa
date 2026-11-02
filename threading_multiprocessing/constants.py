"""Shared values for config, timestamp files, and Yahoo Finance fetches."""

import logging

DEFAULT_TICKERS = ("BTC", "GOOGL", "AMZN")

ENV_DESTINATION_FILE_PATH = "DESTINATION_FILE_PATH"
ENV_MAX_WORKERS = "MAX_WORKERS"
DEFAULT_DESTINATION_FILE_PATH = "output.csv"
DEFAULT_MAX_WORKERS = 10
MIN_WORKERS = 1

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
TIMESTAMP_FLOOR = "min"
TIMESTAMP_FILE_SUFFIX = ".txt"
TIMESTAMP_INDEX_NAME = "timestamp"

OHLCV_COLUMNS = ("Open", "High", "Low", "Close", "Volume")
OHLCV_DTYPES = {
    "Open": float,
    "High": float,
    "Low": float,
    "Close": float,
    "Volume": int,
}

FETCH_INTERVAL = "1m"
MAX_FETCH_DAYS = 30
CHUNK_DAYS = 7
FETCH_TIMEZONE = "UTC"

REPORT_COLUMNS = ("timestamp", "stock_type", "price_change")

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S"
EXIT_CODE_FAILURE = 1
