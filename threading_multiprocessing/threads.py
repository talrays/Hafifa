"""Thread-pool helper for I/O-bound work (Yahoo downloads)."""

import concurrent.futures
from logging import getLogger
from typing import Callable
from typing import TypeVar

logger = getLogger(__name__)


T = TypeVar("T")
# (callable, args, kwargs)
Job = tuple[Callable[..., T], tuple, dict]

def run_in_parallel(jobs: list[Job], max_workers: int) -> list[concurrent.futures.Future[T]]:
    """Run ``jobs`` concurrently and return futures in submission order.

    Args:
        jobs: Each entry is ``(callable, args_tuple, kwargs_dict)``.
        max_workers: ``ThreadPoolExecutor`` pool size.

    Returns:
        Futures aligned with ``jobs``. The pool waits for all tasks before
        returning. An empty ``jobs`` list yields ``[]``.

    Note:
        Exceptions are stored on the future; callers must call ``Future.result()``
        to surface them.
    """
    if not jobs:
        return []
    logger.info("Running %d jobs in thread pool (max_workers=%d)", len(jobs), max_workers)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(func, *args, **kwargs) for func, args, kwargs in jobs]
        concurrent.futures.wait(futures)
        return futures
