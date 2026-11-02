"""Build and write the combined price-change CSV for all tickers."""

from pathlib import Path

import pandas as pd
from logging import getLogger
from models import Stock
from constants import REPORT_COLUMNS, TIMESTAMP_INDEX_NAME
from utils import minute_price_change_pct

logger = getLogger(__name__)


def write_report(destination_file_path: str, report: pd.DataFrame) -> None:
    """Write ``report`` as CSV with ``REPORT_COLUMNS`` and no index.

    Creates parent directories when the destination path includes folders
    (for example ``output/output.csv``).
    """
    destination = Path(destination_file_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(destination, index=False, columns=list(REPORT_COLUMNS))
    logger.info(f"Report written to {destination_file_path} ({len(report)} rows)")


def build_report(stocks: list[Stock]) -> pd.DataFrame:
    """Assemble one combined report frame from all ``stocks``.

    Includes only required minutes that have matching OHLCV bars. Tickers with
    no matches contribute no rows. Returns an empty frame with ``REPORT_COLUMNS``
    when every slice is empty.
    """
    slices: list[pd.DataFrame] = []
    for stock in stocks:
        ohlcv = stock.get_required_data()
        logger.info(
            f"Report slice {stock.ticker.value}: {len(ohlcv)} rows for required minutes"
        )
        if ohlcv.empty:
            continue
        slices.append(
            pd.DataFrame(
                {
                    TIMESTAMP_INDEX_NAME: ohlcv.index,
                    "stock_type": stock.ticker.value,
                    "price_change": minute_price_change_pct(ohlcv).values,
                }
            )
        )
    if not slices:
        return pd.DataFrame(columns=list(REPORT_COLUMNS))
    return pd.concat(slices, ignore_index=True)[list(REPORT_COLUMNS)]
