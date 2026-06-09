import hashlib
import sys
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.fetch_source_archive import fetch_source_archive
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
        self.offset = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self, size=-1):
        if self.offset >= len(self.payload):
            return b""
        if size < 0:
            size = len(self.payload) - self.offset
        chunk = self.payload[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk


class FetchSourceArchiveTest(unittest.TestCase):
    def test_fetch_source_archive_writes_and_verifies_hash(self):
        payload = b"source zip bytes"
        expected = hashlib.sha256(payload).hexdigest()
        output = TEST_TMP / f"source_{uuid.uuid4().hex}.zip"

        result = fetch_source_archive(
            url="https://example.invalid/source.zip",
            output_path=output,
            expected_sha256=expected,
            opener=lambda url: FakeResponse(payload),
        )

        self.assertEqual(result["sha256"], expected)
        self.assertEqual(output.read_bytes(), payload)

    def test_fetch_source_archive_adds_bearer_token_when_present(self):
        payload = b"source zip bytes"
        expected = hashlib.sha256(payload).hexdigest()
        output = TEST_TMP / f"source_auth_{uuid.uuid4().hex}.zip"
        requests = []

        def opener(request):
            requests.append(request)
            return FakeResponse(payload)

        result = fetch_source_archive(
            url="https://huggingface.co/datasets/example/source/resolve/main/source.zip",
            output_path=output,
            expected_sha256=expected,
            token="hf_test",
            opener=opener,
        )

        self.assertEqual(result["sha256"], expected)
        self.assertEqual(requests[0].headers["Authorization"], "Bearer hf_test")

    def test_fetch_source_archive_deletes_bad_hash_download(self):
        output = TEST_TMP / f"source_bad_{uuid.uuid4().hex}.zip"

        with self.assertRaises(ValueError):
            fetch_source_archive(
                url="https://example.invalid/source.zip",
                output_path=output,
                expected_sha256="0" * 64,
                opener=lambda url: FakeResponse(b"wrong"),
            )

        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
