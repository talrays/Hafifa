"""Turn per-ticker frames into the destination CSV."""

import pandas as pd
from logging import getLogger
from models import Stock
from constants import TIMESTAMP_INDEX_NAME

logger = getLogger(__name__)

def write_report(destination_file_path: str, report: pd.DataFrame)->None:
    """Write ``report`` to ``destination_file_path`` without the index."""
    report.to_csv(destination_file_path, index=False)
    logger.info("Report written to %s (%d rows)", destination_file_path, len(report))

def build_report(stocks: list[Stock]) -> pd.DataFrame:
    """Concatenate ``get_required_data()`` for each stock, in list order.

    The minute index becomes the leading ``timestamp`` column.
    """
    report = pd.DataFrame()
    for stock in stocks:
        slice_frame = stock.get_required_data()
        logger.info(
            "Report slice %s: %d rows for required minutes",
            stock.ticker.value,
            len(slice_frame),
        )
        report = pd.concat([report, slice_frame])
    return report.rename_axis(TIMESTAMP_INDEX_NAME).reset_index()
