from __future__ import annotations

import unittest
from unittest.mock import patch

from scripts.http_retry import call_with_retries


class HttpRetryTests(unittest.TestCase):
    def test_call_with_retries_retries_retryable_exception(self) -> None:
        attempts = {"count": 0}

        def flaky() -> str:
            attempts["count"] += 1
            if attempts["count"] == 1:
                raise TimeoutError("temporary")
            return "ok"

        with patch("scripts.http_retry.time.sleep", return_value=None):
            result = call_with_retries(
                flaky,
                should_retry=lambda exc: isinstance(exc, TimeoutError),
            )

        self.assertEqual(result, "ok")
        self.assertEqual(attempts["count"], 2)

    def test_call_with_retries_does_not_retry_non_retryable_exception(self) -> None:
        attempts = {"count": 0}

        def failing() -> str:
            attempts["count"] += 1
            raise ValueError("not transient")

        with self.assertRaises(ValueError):
            call_with_retries(failing, should_retry=lambda exc: isinstance(exc, TimeoutError))

        self.assertEqual(attempts["count"], 1)


if __name__ == "__main__":
    unittest.main()
