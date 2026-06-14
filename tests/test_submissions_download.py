"""Tests for document download functions."""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.parliament_submissions.download import (
    download_pdf,
    download_pdf_with_retry,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class FakeResponse:
    def __init__(self, payload: bytes, status: int = 200):
        self.payload = payload
        self.status = status
        self.offset = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, size: int = -1) -> bytes:
        if self.offset >= len(self.payload):
            return b""
        if size < 0:
            size = len(self.payload) - self.offset
        chunk = self.payload[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk

    def getcode(self) -> int:
        return self.status


class FakeOpener:
    def __init__(self, payload: bytes, status: int = 200):
        self.payload = payload
        self.status = status
        self.requests: list = []

    def __call__(self, request):
        self.requests.append(request)
        return FakeResponse(self.payload, self.status)


class DownloadPdfTest(unittest.TestCase):

    def test_download_pdf_writes_file(self):
        payload = b"%PDF-1.4 fake content"
        out = TEST_TMP / "test_download.pdf"
        opener = FakeOpener(payload)

        result = download_pdf(
            url="https://example.com/submission.pdf",
            output_path=out,
            opener=opener,
        )

        self.assertTrue(out.exists())
        self.assertEqual(out.read_bytes(), payload)
        self.assertEqual(result["path"], str(out))
        self.assertEqual(result["bytes"], len(payload))
        self.assertEqual(result["status"], 200)

    def test_download_pdf_returns_sha256(self):
        payload = b"PDF content for hash check"
        out = TEST_TMP / "test_hash.pdf"
        opener = FakeOpener(payload)

        result = download_pdf(
            url="https://example.com/submission.pdf",
            output_path=out,
            opener=opener,
        )

        self.assertIn("sha256", result)
        expected = hashlib.sha256(payload).hexdigest()
        self.assertEqual(result["sha256"], expected)

    def test_download_pdf_missing_url_returns_error(self):
        result = download_pdf(
            url="",
            output_path=TEST_TMP / "empty_url.pdf",
        )
        self.assertIn("error", result)
        self.assertEqual(result["status"], 0)

    def test_download_pdf_handles_http_error(self):
        result = download_pdf(
            url="https://example.invalid/submission.pdf",
            output_path=TEST_TMP / "http_err.pdf",
        )
        self.assertIn("error", result)

    def test_download_pdf_with_retry_succeeds(self):
        payload = b"PDF content"
        out = TEST_TMP / "retry_ok.pdf"
        opener = FakeOpener(payload)

        result = download_pdf_with_retry(
            url="https://example.com/submission.pdf",
            output_path=out,
            max_retries=2,
            opener=opener,
        )

        self.assertTrue(out.exists())
        self.assertEqual(result["status"], 200)
        self.assertIn("sha256", result)

    def test_retry_fails_after_exhaustion(self):
        class FailingOpener:
            def __call__(self, request):
                raise ConnectionError("Connection refused")

        result = download_pdf_with_retry(
            url="https://example.com/submission.pdf",
            output_path=TEST_TMP / "retry_fail.pdf",
            max_retries=2,
            opener=FailingOpener(),
        )

        self.assertIn("error", result)
        self.assertIn("retries_exhausted", result.get("error", ""))

    def test_retry_records_attempts(self):
        payload = b"PDF"
        out = TEST_TMP / "retry_attempts.pdf"
        opener = FakeOpener(payload)

        result = download_pdf_with_retry(
            url="https://example.com/submission.pdf",
            output_path=out,
            max_retries=2,
            opener=opener,
        )

        self.assertIn("attempts", result)
        self.assertGreaterEqual(result["attempts"], 1)


class DownloadPdfIntegrationTest(unittest.TestCase):
    """Integration tests that actually make HTTP requests."""

    def test_download_with_nonexistent_url(self):
        """Should handle a 404 or unresolvable URL gracefully."""
        result = download_pdf(
            url="https://nonexistent.example.com/submission.pdf",
            output_path=TEST_TMP / "integration_404.pdf",
        )
        self.assertIn("error", result)
        self.assertNotEqual(result.get("status", 0), 200)


if __name__ == "__main__":
    unittest.main()

