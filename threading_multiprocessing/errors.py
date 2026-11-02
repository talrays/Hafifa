"""Typed exceptions for download and pipeline boundaries.

These are raised inside the library and logged in ``main`` or ``run_pipeline``
before the process exits or before a partial CSV is written.
"""


class DownloadError(Exception):
    """No usable OHLCV chunks for one ticker; typically wrapped in ``PipelineError``."""


class PipelineError(Exception):
    """Pipeline stopped before a successful report write.

    Raised when a ticker's fetch window is invalid, one or more downloads fail,
    or report build/write fails.
    """
