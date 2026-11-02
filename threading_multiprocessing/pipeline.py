"""Orchestrate timestamp loading, parallel Yahoo fetches, and CSV output.

``run_pipeline`` is the only public entry point. It validates each ticker's
fetch window, downloads OHLCV in parallel, builds ``Stock`` instances from each
result, and writes the combined report.
"""

from logging import getLogger

import pandas as pd

from config import Config
from loader import read_timestamps_from_txt
from models import Stock, StockTicker
from client import get_stock_data, validate_date_range
from threads import run_in_parallel
from report import write_report, build_report
from errors import PipelineError
from constants import MAX_FETCH_DAYS

logger = getLogger(__name__)

def run_pipeline(config: Config) -> None:
    """Load timestamps, fetch OHLCV for each ticker, and write the CSV report.

    For each ticker, required minutes are read from ``config.timestamps_file_path_dict``,
    the min/max minute define the Yahoo window, and ``validate_date_range`` must pass
    before a download job is queued. Jobs run in a pool of ``config.max_workers``
    threads; futures are consumed in ticker order after all jobs complete.

    Raises:
        PipelineError: When any ticker's window is invalid, any fetch fails, or
            report building or writing fails. Failures are summarized in the message;
            per-ticker errors are also logged at ERROR.
        FileNotFoundError: When a timestamp file is missing (from the loader).
        ValueError: When a timestamp file is empty or malformed (from the loader).
    """
    logger.info("Starting pipeline")
    fetch_jobs = []
    load_specs: list[tuple[StockTicker, pd.Series]] = []
    window_failures: list[tuple[str, Exception]] = []
    for ticker in config.stock_tickers:
        path = config.timestamps_file_path_dict[ticker]
        timestamps = read_timestamps_from_txt(path)
        start, end = timestamps.min(), timestamps.max()
        try:
            validate_date_range(start, end)
        except ValueError as exc:
            logger.error(
                "%s timestamps in %s span %s to %s; Yahoo only serves the last %s days: %s",
                ticker.value,
                path,
                start,
                end,
                MAX_FETCH_DAYS,
                exc,
            )
            window_failures.append((ticker.value, exc))
            continue
        logger.info(
            "Loaded %s: %d required minutes from %s (fetch window %s to %s)",
            ticker.value,
            len(timestamps),
            path,
            start,
            end,
        )
        load_specs.append((ticker, timestamps))
        fetch_jobs.append((get_stock_data, (ticker, start, end), {}))

    if window_failures:
        summary = "; ".join(f"{ticker}: {exc}" for ticker, exc in window_failures)
        raise PipelineError(summary)

    futures = run_in_parallel(fetch_jobs, config.max_workers)
    results = []
    failures: list[tuple[str, Exception]] = []
    for (ticker, _timestamps), future in zip(load_specs, futures):
        try:
            results.append(future.result())
        except Exception as exc:
            logger.error("Fetch failed for %s: %s", ticker.value, exc)
            failures.append((ticker.value, exc))

    if failures:
        summary = "; ".join(f"{ticker}: {exc}" for ticker, exc in failures)
        raise PipelineError(summary)

    stocks: list[Stock] = []
    for (ticker, timestamps), data in zip(load_specs, results):
        stock = Stock(ticker, timestamps, data)
        stocks.append(stock)
        matched = len(stock.get_required_data())
        logger.info(
            "Built %s: %d downloaded bars, %d rows match required minutes",
            ticker.value,
            len(data),
            matched,
        )
    logger.info("Building report for %d tickers", len(stocks))
    try:
        report = build_report(stocks)
        write_report(config.destination_file_path, report)
    except Exception as exc:
        logger.error("Report failed: %s", exc)
        raise PipelineError(f"Report failed: {exc}")
        
    logger.info("Pipeline completed successfully")
