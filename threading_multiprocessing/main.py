"""Entry point: load settings from the environment and run the stock pipeline."""

import sys
import warnings
from logging import getLogger, basicConfig
from pydantic import ValidationError

from pipeline import run_pipeline
from settings import Settings
from errors import PipelineError
from constants import LOG_DATE_FORMAT, LOG_FORMAT, LOG_LEVEL


basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
# Must run after yfinance is imported: its __init__ re-enables its own DeprecationWarnings.
warnings.filterwarnings(
    "ignore",
    message="The 'generic' unit for NumPy timedelta is deprecated",
    category=DeprecationWarning,
    module="yfinance",
)
logger = getLogger(__name__)

def main() -> int:
    try:
        settings = Settings()
        run_pipeline(settings)
        return 0  # Success code
    except (ValidationError, PipelineError) as exc:
        logger.error(f"Failure: {exc}")
        return 1  # Failure code
    except Exception as exc:
        logger.exception(f"Unexpected error: {exc}")
        return 1  # Failure code

if __name__ == "__main__":
    logger.info("Starting main")
    sys.exit(main())
