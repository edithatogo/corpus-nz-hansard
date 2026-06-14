"""Tests for NZ Parliament select committee submissions scraper."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.parliament_submissions.scraper import (
    fetch_submissions_list,
    parse_submission_list,
    SubmissionEntry,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()

API_RESPONSE = {
    "results": [
        {"id": "sub-001", "title": "Submission on ABC Bill",
         "submitter": "Jane Citizen", "committee": "Justice Committee",
         "billReference": "ABC Bill", "submissionDate": "2024-03-15",
         "documentUrl": "/en/pb/sc/sub-001.pdf", "status": "received"},
        {"id": "sub-002", "title": "Submission on XYZ Bill",
         "submitter": "Organisation NZ", "committee": "Health Committee",
         "billReference": "XYZ Bill", "submissionDate": "2024-04-01",
         "documentUrl": "/en/pb/sc/sub-002.pdf", "status": "received"},
    ],
    "totalResults": 2, "page": 1, "pageSize": 50,
}

HTML_RESPONSE = """<html><body>
<div class="submission-item">
  <h3>Submission on ABC Bill</h3>
  <p class="submitter">Jane Citizen</p>
  <p class="committee">Justice Committee</p>
  <p class="date">2024-03-15</p>
  <a href="/en/pb/sc/sub-001.pdf">Download</a>
</div>
<div class="submission-item">
  <h3>Submission on XYZ Bill</h3>
  <p class="submitter">Organisation NZ</p>
  <p class="committee">Health Committee</p>
  <p class="date">2024-04-01</p>
  <a href="/en/pb/sc/sub-002.pdf">Download</a>
</div>
</body></html>"""


class FakeResponse:
    def __init__(self, payload, status=200):
        self.payload = payload.encode("utf-8") if isinstance(payload, str) else payload
        self.status = status
        self.offset = 0

    def __enter__(self): return self
    def __exit__(self, *a): return False
    def read(self, size=-1):
        if self.offset >= len(self.payload): return b""
        if size < 0: size = len(self.payload) - self.offset
        chunk = self.payload[self.offset:self.offset + size]
        self.offset += len(chunk)
        return chunk
    def getcode(self): return self.status


class FakeOpener:
    def __init__(self, payload, status=200):
        self.payload = payload; self.status = status; self.request = None
    def __call__(self, request):
        self.request = request
        return FakeResponse(self.payload, self.status)


class FetchSubmissionsListTest(unittest.TestCase):

    def test_fetch_returns_json(self):
        opener = FakeOpener(json.dumps(API_RESPONSE))
        result = fetch_submissions_list(
            url="https://committees.parliament.nz/api/submissions", opener=opener)
        self.assertEqual(len(result.get("results", [])), 2)
        self.assertEqual(result["totalResults"], 2)

    def test_fetch_pagination_params(self):
        opener = FakeOpener(json.dumps({"results": [], "totalResults": 0}))
        fetch_submissions_list(
            url="https://committees.parliament.nz/api/submissions",
            page=2, page_size=100, opener=opener)
        import urllib.parse
        full = str(opener.request.full_url)
        params = urllib.parse.parse_qs(urllib.parse.urlparse(full).query)
        self.assertEqual(params.get("page"), ["2"])
        self.assertEqual(params.get("pageSize"), ["100"])

    def test_fetch_http_error(self):
        result = fetch_submissions_list(
            url="https://committees.parliament.nz/api/submissions",
            opener=FakeOpener("Not Found", status=404))
        self.assertIn("error", result)


class ParseSubmissionListTest(unittest.TestCase):

    def test_parse_json(self):
        entries = parse_submission_list(API_RESPONSE)
        self.assertEqual(len(entries), 2)
        e = entries[0]
        self.assertEqual(e.id, "sub-001")
        self.assertEqual(e.submitter, "Jane Citizen")
        self.assertEqual(e.committee, "Justice Committee")
        self.assertEqual(e.bill_reference, "ABC Bill")
        self.assertEqual(e.submission_date, "2024-03-15")

    def test_parse_html(self):
        entries = parse_submission_list(HTML_RESPONSE, source="html")
        self.assertGreaterEqual(len(entries), 2)
        submitters = [e.submitter for e in entries if e.submitter]
        self.assertIn("Jane Citizen", submitters)

    def test_parse_empty(self):
        self.assertEqual(parse_submission_list({"results": [], "totalResults": 0}), [])

    def test_parse_missing_fields(self):
        entries = parse_submission_list({"results": [{"id": "sub-003"}]})
        self.assertEqual(len(entries), 1)
        self.assertIsNone(entries[0].submitter)
        self.assertIsNone(entries[0].committee)

    def test_entry_to_dict(self):
        e = SubmissionEntry(id="s", title="T", submitter="P", committee="C",
                            bill_reference="B", submission_date="2024-01-01",
                            document_url="/d.pdf", status="received")
        d = e.to_dict()
        self.assertEqual(d["id"], "s")
        self.assertEqual(d["submitter"], "P")

    def test_minimal_entry(self):
        e = SubmissionEntry(id="sub-min")
        self.assertEqual(e.id, "sub-min")
        self.assertIsNone(e.title)

    def test_absolute_url(self):
        e = SubmissionEntry(id="s", document_url="/en/pb/sc/doc.pdf")
        self.assertEqual(e.absolute_url("https://www.parliament.nz"),
                         "https://www.parliament.nz/en/pb/sc/doc.pdf")


if __name__ == "__main__":
    unittest.main()

