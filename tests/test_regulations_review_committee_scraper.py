"""Tests for Regulations Review Committee proceedings scraper."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.regulations_review_committee.scraper import (
    fetch_proceedings_index,
    parse_proceeding_list,
    ProceedingEntry,
    fetch_proceeding_document,
)

from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()

API_RESPONSE = {
    "results": [
        {
            "id": "proc-001",
            "title": "Regulations Review Committee - 2024-03-15",
            "meetingDate": "2024-03-15",
            "committee": "Regulations Review Committee",
            "documentUrl": "/en/pb/sc/scl/regulations-review-committee/document/proc-001.pdf",
            "documentType": "proceedings",
            "agendaItems": ["Review of Subordinate Legislation", "Complaint re: ABC Regulations"],
            "status": "published",
        },
    ],
    "totalResults": 1,
    "page": 1,
    "pageSize": 50,
}

HTML_RESPONSE = """<html><body>
<div class="proceeding-item">
  <h3>Regulations Review Committee - 2024-03-15</h3>
  <p class="meeting-date">2024-03-15</p>
  <p class="committee">Regulations Review Committee</p>
  <ul class="agenda-items">
    <li>Review of Subordinate Legislation</li>
    <li>Complaint re: ABC Regulations</li>
  </ul>
  <a href="/en/pb/sc/scl/regulations-review-committee/document/proc-001.pdf">Download Minutes</a>
</div>
</body></html>"""


class FakeResponse:
    def __init__(self, payload, status=200):
        self.payload = payload.encode("utf-8") if isinstance(payload, str) else payload
        self.status = status
        self.offset = 0

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self, size=-1):
        if self.offset >= len(self.payload):
            return b""
        if size < 0:
            size = len(self.payload) - self.offset
        chunk = self.payload[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk

    def getcode(self):
        return self.status


class FakeOpener:
    def __init__(self, payload, status=200):
        self.payload = payload
        self.status = status
        self.request = None

    def __call__(self, request):
        self.request = request
        return FakeResponse(self.payload, self.status)




class FetchProceedingsIndexTest(unittest.TestCase):

    def test_fetch_returns_json(self):
        opener = FakeOpener(json.dumps(API_RESPONSE))
        result = fetch_proceedings_index(
            url="https://committees.parliament.nz/api/committees/regulations-review/proceedings",
            opener=opener,
        )
        self.assertEqual(len(result.get("results", [])), 1)
        self.assertEqual(result["totalResults"], 1)

    def test_fetch_pagination_params(self):
        opener = FakeOpener(json.dumps({"results": [], "totalResults": 0}))
        fetch_proceedings_index(
            url="https://committees.parliament.nz/api/committees/regulations-review/proceedings",
            page=3,
            page_size=25,
            opener=opener,
        )
        import urllib.parse
        full = str(opener.request.full_url)
        params = urllib.parse.parse_qs(urllib.parse.urlparse(full).query)
        self.assertEqual(params.get("page"), ["3"])
        self.assertEqual(params.get("pageSize"), ["25"])

    def test_fetch_with_date_filter(self):
        opener = FakeOpener(json.dumps({"results": [], "totalResults": 0}))
        fetch_proceedings_index(
            url="https://committees.parliament.nz/api/committees/regulations-review/proceedings",
            from_date="2024-01-01",
            to_date="2024-12-31",
            opener=opener,
        )
        import urllib.parse
        full = str(opener.request.full_url)

class ParseProceedingListTest(unittest.TestCase):

    def test_parse_json(self):
        entries = parse_proceeding_list(API_RESPONSE)
        self.assertEqual(len(entries), 1)
        e = entries[0]
        self.assertEqual(e.id, "proc-001")
        self.assertEqual(e.meeting_date, "2024-03-15")
        self.assertEqual(e.committee, "Regulations Review Committee")
        self.assertIn("Review of Subordinate Legislation", e.agenda_items)

    def test_parse_html(self):
        entries = parse_proceeding_list(HTML_RESPONSE, source="html")
        self.assertGreaterEqual(len(entries), 1)
        self.assertEqual(entries[0].meeting_date, "2024-03-15")
        self.assertIn("Review of Subordinate Legislation", entries[0].agenda_items)

    def test_parse_empty(self):
        self.assertEqual(parse_proceeding_list({"results": [], "totalResults": 0}), [])

    def test_parse_missing_fields(self):
        entries = parse_proceeding_list({"results": [{"id": "proc-003"}]})
        self.assertEqual(len(entries), 1)
        self.assertIsNone(entries[0].meeting_date)
        self.assertIsNone(entries[0].committee)
        self.assertEqual(entries[0].agenda_items, [])

    def test_entry_to_dict(self):
        e = ProceedingEntry(
            id="proc-001",
            title="Regulations Review Committee - 2024-03-15",
            meeting_date="2024-03-15",
            committee="Regulations Review Committee",
            document_url="/en/pb/sc/scl/regulations-review-committee/document/proc-001.pdf",
            document_type="proceedings",
            agenda_items=["Item 1", "Item 2"],
            status="published",
        )
        d = e.to_dict()
        self.assertEqual(d["id"], "proc-001")
        self.assertEqual(d["meeting_date"], "2024-03-15")
        self.assertIn("Item 1", d["agenda_items"])

    def test_minimal_entry(self):
        e = ProceedingEntry(id="proc-min")
        self.assertEqual(e.id, "proc-min")
        self.assertIsNone(e.title)
        self.assertEqual(e.agenda_items, [])


class FetchProceedingDocumentTest(unittest.TestCase):

    def test_fetch_document_success(self):
        pdf_content = b"%PDF-1.4 fake content"
        opener = FakeOpener(pdf_content)
        result = fetch_proceeding_document(
            url="https://www.parliament.nz/en/pb/sc/doc.pdf",
            output_path=TEST_TMP / "doc.pdf",
            opener=opener,
        )
        self.assertIn("path", result)
        self.assertIn("bytes", result)
        self.assertIn("sha256", result)
        self.assertIn("status", result)
        self.assertTrue((TEST_TMP / "doc.pdf").exists())

    def test_fetch_document_empty_url(self):
        result = fetch_proceeding_document(
            url="", output_path=TEST_TMP / "empty.pdf"
        )
        self.assertIn("error", result)
        self.assertEqual(result["status"], 0)

    def test_fetch_document_http_error(self):
        result = fetch_proceeding_document(
            url="https://example.com/missing.pdf",
            output_path=TEST_TMP / "missing.pdf",
            opener=FakeOpener("", status=404),
        )
        self.assertEqual(result.get("status"), 404)

    def test_fetch_document_verifies_content(self):
        pdf_content = b"%PDF-1.4 valid header"
        opener = FakeOpener(pdf_content)
        result = fetch_proceeding_document(
            url="https://www.parliament.nz/en/pb/sc/valid.pdf",
            output_path=TEST_TMP / "valid.pdf",
            opener=opener,
        )
        self.assertIn("sha256", result)
        self.assertGreater(result["bytes"], 0)


if __name__ == "__main__":
    unittest.main()

    def test_absolute_url(self):
        e = ProceedingEntry(id="proc-001", document_url="/en/pb/sc/doc.pdf")
        self.assertEqual(
            e.absolute_url("https://www.parliament.nz"),
            "https://www.parliament.nz/en/pb/sc/doc.pdf",
        )

        params = urllib.parse.parse_qs(urllib.parse.urlparse(full).query)
        self.assertEqual(params.get("fromDate"), ["2024-01-01"])
        self.assertEqual(params.get("toDate"), ["2024-12-31"])

    def test_fetch_http_error(self):
        result = fetch_proceedings_index(
            url="https://committees.parliament.nz/api/committees/regulations-review/proceedings",
            opener=FakeOpener("Not Found", status=404),
        )
        self.assertIn("error", result)

    def test_fetch_html_fallback(self):
        opener = FakeOpener(HTML_RESPONSE)
        result = fetch_proceedings_index(
            url="https://www.parliament.nz/en/pb/sc/scl/regulations-review-committee/proceedings",
            source="html",
            opener=opener,
        )
        self.assertIn("results", result)
        self.assertEqual(len(result["results"]), 1)
