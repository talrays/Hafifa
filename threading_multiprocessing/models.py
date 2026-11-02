"""Domain models: ticker symbols and per-ticker OHLCV plus required minutes."""

from enum import Enum
import pandas as pd
from dataclasses import dataclass, field
from datetime import datetime
from constants import OHLCV_DTYPES, TIMESTAMP_INDEX_NAME


class StockTicker(Enum):
    """Symbols fetched from Yahoo Finance and used as timestamp filenames."""

    BTC = "BTC"
    GOOGL = "GOOGL"
    AMZN = "AMZN"


def create_empty_ohlcv() -> pd.DataFrame:
    """Empty Open/High/Low/Close/Volume frame indexed by timestamp."""
    return pd.DataFrame(
        {column: pd.Series(dtype) for column, dtype in OHLCV_DTYPES.items()},
        index=pd.DatetimeIndex([], name=TIMESTAMP_INDEX_NAME),
    ) 

    
@dataclass
class Stock:
    """One ticker, the bars downloaded for it, and the minutes the report needs."""

    ticker: StockTicker
    data: pd.DataFrame = field(default_factory=create_empty_ohlcv)
    required_timestamps: pd.Series = field(default_factory=pd.Series)
    
    def add_data(self, data: pd.DataFrame) -> None:
        """Merge downloaded OHLCV rows into ``data`` (no-op when ``data`` is empty)."""
        if data.empty:
            return
        self.data = data if self.data.empty else pd.concat([self.data, data])
    
    def add_timestamps(self, timestamps: pd.Series) -> None:
        """Append minutes that must appear in the final CSV."""
        self.required_timestamps = pd.concat([self.required_timestamps, timestamps])

    def get_required_data(self) -> pd.DataFrame:
        """OHLCV rows whose index is listed in ``required_timestamps``."""
        return self.data.loc[self.data.index.isin(self.required_timestamps)]


    def get_required_timestamps(self) -> pd.Series:
        """Required report minutes for this ticker (may include duplicates)."""
        return self.required_timestamps
    
    def get_min_required_timestamp(self) -> datetime:
        """Earliest required minute. Used as the Yahoo download start."""
        return self.required_timestamps.min()

    def get_max_required_timestamp(self) -> datetime:
        """Latest required minute. Used as the Yahoo download end."""
        return self.required_timestamps.max()

