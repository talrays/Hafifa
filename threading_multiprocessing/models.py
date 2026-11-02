"""Domain models: ticker symbols and per-ticker OHLCV plus required minutes."""

from enum import Enum

import pandas as pd


class StockTicker(Enum):
    """Symbols fetched from Yahoo Finance and used as timestamp filenames."""

    BTC = "BTC"
    GOOGL = "GOOGL"
    AMZN = "AMZN"


class Stock:
    """One ticker, downloaded OHLCV, and the minutes that must appear in the report."""

    def __init__(
        self,
        ticker: StockTicker,
        required_timestamps: pd.Series,
        data: pd.DataFrame,
    ) -> None:
        self.ticker = ticker
        self.required_timestamps = required_timestamps
        self.data = data

    def get_required_data(self) -> pd.DataFrame:
        """OHLCV rows whose index is listed in ``required_timestamps``."""
        return self.data.loc[self.data.index.isin(self.required_timestamps)]
