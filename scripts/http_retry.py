"""Small retry helpers for repository-controlled HTTP acquisition scripts."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request

import requests

RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


def _sleep_seconds(attempt: int, base_delay: float) -> float:
    return base_delay * (2 ** (attempt - 1))


def call_with_retries[T](
    call: Callable[[], T],
    *,
    attempts: int = 3,
    base_delay: float = 1.0,
    should_retry: Callable[[BaseException], bool] | None = None,
) -> T:
    """Run ``call`` with bounded exponential backoff."""
    if attempts < 1:
        msg = "attempts must be at least 1"
        raise ValueError(msg)

    last_error: BaseException | None = None
    for attempt in range(1, attempts + 1):
        try:
            return call()
        except BaseException as exc:
            if should_retry is not None and not should_retry(exc):
                raise
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(_sleep_seconds(attempt, base_delay))

    if last_error is None:
        msg = "retry call failed without an exception"
        raise RuntimeError(msg)
    raise last_error


def _retry_requests_error(exc: BaseException) -> bool:
    if isinstance(exc, requests.HTTPError):
        response = exc.response
        return response is not None and response.status_code in RETRYABLE_STATUS_CODES
    return isinstance(exc, (requests.ConnectionError, requests.Timeout))


def request_with_retries(
    method: str,
    url: str,
    *,
    attempts: int = 3,
    base_delay: float = 1.0,
    session: requests.Session | None = None,
    **kwargs: Any,
) -> requests.Response:
    """Perform a requests call with retries for transient failures."""
    client = session or requests

    def _call() -> requests.Response:
        response = client.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    return call_with_retries(
        _call,
        attempts=attempts,
        base_delay=base_delay,
        should_retry=_retry_requests_error,
    )


def _retry_urlopen_error(exc: BaseException) -> bool:
    if isinstance(exc, HTTPError):
        return exc.code in RETRYABLE_STATUS_CODES
    return isinstance(exc, URLError)


def urlopen_bytes_with_retries(
    request: Request,
    *,
    opener: Callable[..., Any],
    timeout: int = 60,
    attempts: int = 3,
    base_delay: float = 1.0,
) -> bytes:
    """Read bytes from ``urlopen`` with retries for transient failures."""

    def _call() -> bytes:
        with opener(request, timeout=timeout) as response:
            return response.read()

    return call_with_retries(
        _call,
        attempts=attempts,
        base_delay=base_delay,
        should_retry=_retry_urlopen_error,
    )
