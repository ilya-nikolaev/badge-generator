import functools
import logging
import time
from collections.abc import Awaitable, Callable
from typing import ParamSpec, TypeVar

logger = logging.getLogger(__name__)

P = ParamSpec("P")
T = TypeVar("T")


def log_duration(
    label: str,
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    def log_duration(
        f: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[T]]:
        @functools.wraps(f)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            start = time.perf_counter()
            result = await f(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000
            logger.info("%s fetched in %.3f ms", label, duration)
            return result

        return wrapper

    return log_duration
