"""Turn per-ticker frames into the destination CSV."""

import pandas as pd
from logging import getLogger
from models import Stock
from constants import REPORT_COLUMNS, TIMESTAMP_INDEX_NAME

logger = getLogger(__name__)


def minute_price_change_pct(ohlcv: pd.DataFrame) -> pd.Series:
    """Percent move from open to close for each 1m bar."""
    open_price = ohlcv["Open"]
    return (ohlcv["Close"] - open_price) / open_price * 100


def write_report(destination_file_path: str, report: pd.DataFrame) -> None:
    """Write ``report`` to ``destination_file_path`` without the index."""
    report.to_csv(destination_file_path, index=False, columns=list(REPORT_COLUMNS))
    logger.info("Report written to %s (%d rows)", destination_file_path, len(report))


def build_report(stocks: list[Stock]) -> pd.DataFrame:
    """One row per required minute that has OHLCV: timestamp, stock_type, price_change."""
    slices: list[pd.DataFrame] = []
    for stock in stocks:
        ohlcv = stock.get_required_data()
        logger.info(
            "Report slice %s: %d rows for required minutes",
            stock.ticker.value,
            len(ohlcv),
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
