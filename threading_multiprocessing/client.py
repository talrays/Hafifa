"""Download and normalize minute OHLCV bars from Yahoo Finance via yfinance.

Chunked history requests work around Yahoo's short lookback for 1m data.
Callers should treat ``validate_date_range`` failures as fatal for that ticker.
"""

import yfinance as yf
from datetime import datetime
import pandas as pd
from models import StockTicker
from datetime import timedelta
from logging import getLogger
from errors import DownloadError
from constants import CHUNK_DAYS, FETCH_INTERVAL, FETCH_TIMEZONE, MAX_FETCH_DAYS, OHLCV_COLUMNS

logger = getLogger(__name__)


def validate_ohcv(data: pd.DataFrame) -> bool:
    """Return True when every column name is in ``OHLCV_COLUMNS``."""
    return all(data.columns.isin(OHLCV_COLUMNS))


def normalize_ohlcv(raw: pd.DataFrame) -> pd.DataFrame:
    """Subset to OHLCV columns, convert the index to naive UTC, and sort by time."""
    frame = raw.loc[:, list(OHLCV_COLUMNS)].copy()
    if frame.index.tz is not None:
        frame.index = frame.index.tz_convert(FETCH_TIMEZONE).tz_localize(None)
    return frame.sort_index()

def validate_date_range(start: datetime, end: datetime) -> bool:
    """Check that Yahoo can serve 1m bars for ``[start, end]``.

    Returns:
        True when ``start <= end`` and ``end`` is within the last ``MAX_FETCH_DAYS``.

    Raises:
        ValueError: When the range is inverted or ``end`` is too old for Yahoo's
            1m history window.
    """
    if start > end:
        raise ValueError("Start date must be before end date")
    if datetime.now() - end > timedelta(days=MAX_FETCH_DAYS):
        raise ValueError(f"End date must be within the last {MAX_FETCH_DAYS} days")
    return True

def get_stock_data(
    ticker: StockTicker,
    start: datetime,
    end: datetime,
    interval: str = FETCH_INTERVAL,
) -> pd.DataFrame:
    """Download and normalize OHLCV for ``ticker`` between ``start`` and ``end``.

    Requests are split into ``CHUNK_DAYS`` windows. If ``start`` is older than
    ``MAX_FETCH_DAYS`` before now, it is clipped to Yahoo's earliest 1m bar.
    Network errors and empty chunks are logged and skipped; bad column sets fail
    the whole ticker.

    Args:
        ticker: Symbol passed to ``yf.Ticker``.
        start: Inclusive download start (may be clipped).
        end: Upper bound passed to yfinance for the final chunk.
        interval: Bar size (default ``FETCH_INTERVAL``, typically ``1m``).

    Returns:
        Concatenated, sorted frame indexed by bar timestamp with OHLCV columns.

    Raises:
        ValueError: When ``validate_date_range`` fails or a chunk lacks OHLCV columns.
        DownloadError: When every chunk failed or returned no rows.
    """
    validate_date_range(start, end)

    # Yahoo measures its window from now, not from ``end``.
    earliest = datetime.now() - timedelta(days=MAX_FETCH_DAYS)
    if start < earliest:
        logger.warning(
            "Clipping fetch start for %s from %s to %s: Yahoo serves %s data only for the last %s days",
            ticker.value,
            start,
            earliest,
            interval,
            MAX_FETCH_DAYS,
        )
        start = earliest

    data_chunks = []
    chunk_days = CHUNK_DAYS
    current = start
    logger.info("Downloading %s from %s to %s", ticker.value, start, end)

    while current < end:
        current_end = min(current + timedelta(days=chunk_days), end)
        try:
            # yf.download shares module-level state across calls, so it is not thread-safe.
            data = yf.Ticker(ticker.value).history(
                start=current,
                end=current_end,
                interval=interval,
                actions=False,
            )
        except Exception as exc:
            logger.error(
                "Download failed for %s from %s to %s: %s",
                ticker.value,
                current,
                current_end,
                exc,
            )
        else:
            if data is None or data.empty:
                logger.error(
                    "No data for %s from %s to %s",
                    ticker.value,
                    current,
                    current_end,
                )
            elif not validate_ohcv(data):
                raise ValueError(
                    f"Data for {ticker.value} from {current} to {current_end} "
                    "is missing OHLCV columns"
                )
            else:
                data_chunks.append(normalize_ohlcv(data))
        current = current_end

    if not data_chunks:
        raise DownloadError(f"No data downloaded for {ticker.value} from {start} to {end}")
    frame = pd.concat(data_chunks).sort_index()
    logger.info(
        "Downloaded %s: %d bars from %s to %s",
        ticker.value,
        len(frame),
        frame.index.min(),
        frame.index.max(),
    )
    return frame
