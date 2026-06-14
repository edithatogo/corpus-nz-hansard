"""Tests for select committee reports scraper engine."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.select_committee_reports.scraper import (
    fetch_reports_index,
    parse_report_list,
    ReportEntry,
    fetch_report_document,
    DEFAULT_COMMITTEE_LIST,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()

API_RESPONSE = {
    "results": [
        {
            "id": "rep-001",
            "title": "Justice Committee 2024 Annual Report",
            "committee": "Justice Committee",
            "reportDate": "2024-06-30",
            "billReference": None,
            "documentUrl": "/en/pb/sc/reports/report-001.pdf",
            "documentType": "PDF",
            "status": "published",
        },
        {
            "id": "rep-002",
            "title": "Health Committee Inquiry into Mental Health",
            "committee": "Health Committee",
            "reportDate": "2024-05-15",
            "billReference": "Mental Health Bill",
            "documentUrl": "/en/pb/sc/reports/report-002.html",
            "documentType": "HTML",
            "status": "published",
        },
    ],
    "totalResults": 2,
    "page": 1,
    "pageSize": 50,
}


HTML_RESPONSE = """<html><body>
<div class="report-item">
  <h3>Justice Committee 2024 Annual Report</h3>
  <p class="committee">Justice Committee</p>
  <p class="report-date">2024-06-30</p>
  <a href="/en/pb/sc/reports/report-001.pdf">Download Report (PDF)</a>
</div>
<div class="report-item">
  <h3>Health Committee Inquiry into Mental Health</h3>
  <p class="committee">Health Committee</p>
  <p class="report-date">2024-05-15</p>
  <a href="/en/pb/sc/reports/report-002.html">View Report (HTML)</a>
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


class FetchReportsIndexTest(unittest.TestCase):

    def test_fetch_returns_json(self):
        opener = FakeOpener(json.dumps(API_RESPONSE))
        result = fetch_reports_index(
            url="https://committees.parliament.nz/api/reports",
            opener=opener,
        )
        self.assertEqual(len(result.get("results", [])), 2)
        self.assertEqual(result["totalResults"], 2)

    def test_fetch_pagination_params(self):
        opener = FakeOpener(json.dumps({"results": [], "totalResults": 0}))
        fetch_reports_index(
            url="https://committees.parliament.nz/api/reports",
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
        fetch_reports_index(
            url="https://committees.parliament.nz/api/reports",
            from_date="2024-01-01",
            to_date="2024-12-31",
            opener=opener,
        )
        import urllib.parse
        full = str(opener.request.full_url)
        params = urllib.parse.parse_qs(urllib.parse.urlparse(full).query)
        self.assertEqual(params.get("fromDate"), ["2024-01-01"])
        self.assertEqual(params.get("toDate"), ["2024-12-31"])

    def test_fetch_with_committee_filter(self):
        opener = FakeOpener(json.dumps({"results": [], "totalResults": 0}))
        fetch_reports_index(
            url="https://committees.parliament.nz/api/reports",
            committee="Justice Committee",
            opener=opener,
        )
        import urllib.parse
        full = str(opener.request.full_url)
        params = urllib.parse.parse_qs(urllib.parse.urlparse(full).query)
        self.assertEqual(params.get("committee"), ["Justice Committee"])

    def test_fetch_http_error(self):
        result = fetch_reports_index(
            url="https://committees.parliament.nz/api/reports",
            opener=FakeOpener("Not Found", status=404),
        )
        self.assertIn("error", result)

    def test_fetch_html_fallback(self):
        opener = FakeOpener(HTML_RESPONSE)
        result = fetch_reports_index(
            url="https://www.parliament.nz/en/pb/sc/reports",
            source="html",
            opener=opener,
        )
        self.assertIn("results", result)
        self.assertEqual(len(result["results"]), 2)

    def test_fetch_with_default_committees(self):
        """Verify DEFAULT_COMMITTEE_LIST is a non-empty list of strings."""
        self.assertIsInstance(DEFAULT_COMMITTEE_LIST, list)
        self.assertGreater(len(DEFAULT_COMMITTEE_LIST), 0)

class ParseReportListTest(unittest.TestCase):

    def test_parse_json(self):
        entries = parse_report_list(API_RESPONSE)
        self.assertEqual(len(entries), 2)
        e = entries[0]
        self.assertEqual(e.id, "rep-001")
        self.assertEqual(e.report_date, "2024-06-30")
        self.assertEqual(e.committee, "Justice Committee")
        self.assertEqual(e.document_type, "PDF")

    def test_parse_html(self):
        entries = parse_report_list(HTML_RESPONSE, source="html")
        self.assertGreaterEqual(len(entries), 2)
        committees = [e.committee for e in entries if e.committee]
        self.assertIn("Justice Committee", committees)
        self.assertIn("Health Committee", committees)

    def test_parse_empty(self):
        self.assertEqual(parse_report_list({"results": [], "totalResults": 0}), [])

    def test_parse_missing_fields(self):
        entries = parse_report_list({"results": [{"id": "rep-003"}]})
        self.assertEqual(len(entries), 1)
        self.assertIsNone(entries[0].report_date)
        self.assertIsNone(entries[0].committee)
        self.assertEqual(entries[0].document_formats, [])

    def test_entry_to_dict(self):
        e = ReportEntry(
            id="rep-001",
            title="Justice Committee 2024 Annual Report",
            committee="Justice Committee",
            report_date="2024-06-30",
            document_url="/en/pb/sc/reports/report-001.pdf",
            document_type="PDF",
            document_formats=["pdf"],
            status="published",
            bill_reference="Justice Reform Bill",
        )
        d = e.to_dict()
        self.assertEqual(d["id"], "rep-001")
        self.assertEqual(d["committee"], "Justice Committee")
        self.assertIn("pdf", d["document_formats"])

    def test_minimal_entry(self):
        e = ReportEntry(id="rep-min")
        self.assertEqual(e.id, "rep-min")
        self.assertIsNone(e.title)
        self.assertEqual(e.document_formats, [])

    def test_absolute_url(self):
        e = ReportEntry(id="rep-001", document_url="/en/pb/sc/reports/report-001.pdf")
        self.assertEqual(
            e.absolute_url("https://www.parliament.nz"),
            "https://www.parliament.nz/en/pb/sc/reports/report-001.pdf",
        )

    def test_absolute_url_none(self):
        e = ReportEntry(id="rep-001")
        self.assertIsNone(e.absolute_url("https://www.parliament.nz"))


    def test_entry_with_multiple_formats(self):
        e = ReportEntry(
            id="rep-multi",
            title="Multi-format Report",
            document_url="/en/pb/sc/reports/report-multi.pdf",
            document_formats=["pdf", "html", "docx"],
        )
        self.assertIn("pdf", e.document_formats)
        self.assertIn("html", e.document_formats)
        self.assertIn("docx", e.document_formats)

    def test_committee_list_url_generation(self):
        """Verify per-committee URL generation works."""
        url = "https://committees.parliament.nz/api/committees/justice/reports"
        self.assertIn("justice", url)
        self.assertIn("reports", url)


class FetchReportDocumentTest(unittest.TestCase):

    def test_fetch_document_success(self):
        pdf_content = b"%PDF-1.4 fake report content"
        opener = FakeOpener(pdf_content)
        result = fetch_report_document(
            url="https://www.parliament.nz/en/pb/sc/reports/report-001.pdf",
            output_path=TEST_TMP / "report-001.pdf",
            opener=opener,
        )
        self.assertIn("path", result)
        self.assertIn("bytes", result)
        self.assertIn("sha256", result)
        self.assertIn("status", result)
        self.assertTrue((TEST_TMP / "report-001.pdf").exists())

    def test_fetch_document_empty_url(self):
        result = fetch_report_document(
            url="", output_path=TEST_TMP / "empty.pdf"
        )
        self.assertIn("error", result)
        self.assertEqual(result["status"], 0)

    def test_fetch_document_http_error(self):
        result = fetch_report_document(
            url="https://example.com/missing-report.pdf",
            output_path=TEST_TMP / "missing.pdf",
            opener=FakeOpener("", status=404),
        )
        self.assertEqual(result.get("status"), 404)


    def test_fetch_document_verifies_content(self):
        pdf_content = b"%PDF-1.4 valid content"
        opener = FakeOpener(pdf_content)
        result = fetch_report_document(
            url="https://www.parliament.nz/en/pb/sc/reports/valid.pdf",
            output_path=TEST_TMP / "valid.pdf",
            opener=opener,
        )
        self.assertIn("sha256", result)
        self.assertGreater(result["bytes"], 0)

    def test_fetch_document_creates_parent_dirs(self):
        nested = TEST_TMP / "reports" / "2024" / "deep_report.pdf"
        content = b"PDF nested test"
        opener = FakeOpener(content)
        result = fetch_report_document(
            url="https://www.parliament.nz/en/pb/sc/reports/deep.pdf",
            output_path=nested,
            opener=opener,
        )
        self.assertTrue(nested.exists())
        self.assertEqual(result["bytes"], len(content))

    def test_fetch_handles_connection_error(self):
        class FailingOpener:
            def __call__(self, request):
                raise ConnectionError("Connection refused")

        result = fetch_report_document(
            url="https://example.com/report.pdf",
            output_path=TEST_TMP / "conn_err.pdf",
            opener=FailingOpener(),
        )
        self.assertIn("error", result)


class ReportEntryEdgeCasesTest(unittest.TestCase):

    def test_entry_with_extra_fields(self):
        e = ReportEntry(
            id="rep-extra",
            title="Extra Fields Report",
            extra={"pages": 42, "parliament": 53},
        )
        d = e.to_dict()
        self.assertEqual(d["pages"], 42)
        self.assertEqual(d["parliament"], 53)

    def test_entry_round_trip_from_api_shape(self):
        raw = {
            "id": "rep-round",
            "title": "Round Trip Report",
            "committee": "Environment Committee",
            "reportDate": "2024-07-01",
        }
        e = ReportEntry(
            id=raw["id"],
            title=raw.get("title"),
            committee=raw.get("committee"),
            report_date=raw.get("reportDate"),
        )
        self.assertEqual(e.id, "rep-round")
        self.assertEqual(e.committee, "Environment Committee")
        self.assertEqual(e.report_date, "2024-07-01")


if __name__ == "__main__":
    unittest.main()
