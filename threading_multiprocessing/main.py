"""Entry point: load config from the environment and run the stock pipeline."""

import sys
import warnings
from logging import getLogger, basicConfig
from pipeline import run_pipeline
from config import Config
from errors import ConfigError, PipelineError
from constants import EXIT_CODE_FAILURE, LOG_DATE_FORMAT, LOG_FORMAT, LOG_LEVEL


basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
# Must run after yfinance is imported: its __init__ re-enables its own DeprecationWarnings.
warnings.filterwarnings(
    "ignore",
    message="The 'generic' unit for NumPy timedelta is deprecated",
    category=DeprecationWarning,
    module="yfinance",
)
logger = getLogger(__name__)


def main() -> None:
    """Run the pipeline. On a fatal error, log and exit 1."""
    try:
        config = Config.from_env()
        run_pipeline(config)
    except ConfigError as exc:
        logger.error("Invalid configuration: %s", exc)
    except PipelineError as exc:
        logger.error("Pipeline failed: %s", exc)
    except Exception:
        logger.exception("Unexpected error")
    else:
        return
    sys.exit(EXIT_CODE_FAILURE)


if __name__ == "__main__":
    logger.info("Starting main")
    main()
