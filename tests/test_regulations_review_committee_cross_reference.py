"""Tests for regulation cross-referencing and NZ Legislation API integration."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.regulations_review_committee.regulation_cross_reference import (
    SecondaryLegislationKey,
    map_to_legislation_key,
    lookup_nz_legislation,
    build_correlation_index,
    CorrelationEntry,
)
from scripts.regulations_review_committee.complaint_parser import ComplaintRecord


class SecondaryLegislationKeyTest(unittest.TestCase):
    """Tests for SecondaryLegislationKey."""

    def test_sr_key_parsing(self):
        key = SecondaryLegislationKey.from_string("SR 2023/150")
        self.assertEqual(key.prefix, "SR")
        self.assertEqual(key.year, 2023)
        self.assertEqual(key.number, 150)

    def test_li_key_parsing(self):
        key = SecondaryLegislationKey.from_string("LI 2024/56")
        self.assertEqual(key.prefix, "LI")
        self.assertEqual(key.year, 2024)
        self.assertEqual(key.number, 56)

    def test_nzli_key_parsing(self):
        key = SecondaryLegislationKey.from_string("NZLI 2023/100")
        self.assertEqual(key.prefix, "NZLI")
        self.assertEqual(key.year, 2023)
        self.assertEqual(key.number, 100)

    def test_sl_key_parsing(self):
        key = SecondaryLegislationKey.from_string("SL 2024/12")
        self.assertEqual(key.prefix, "SL")
        self.assertEqual(key.year, 2024)
        self.assertEqual(key.number, 12)

    def test_si_key_parsing(self):
        key = SecondaryLegislationKey.from_string("SI 2024/33")
        self.assertEqual(key.prefix, "SI")
        self.assertEqual(key.year, 2024)
        self.assertEqual(key.number, 33)

    def test_plain_year_slash_number(self):
        key = SecondaryLegislationKey.from_string("2023/150")
        self.assertEqual(key.year, 2023)
        self.assertEqual(key.number, 150)

    def test_named_regulation_key(self):
        key = SecondaryLegislationKey.from_string("ABC Regulations 2023")
        self.assertIsNotNone(key)
        self.assertEqual(key.year, 2023)

    def test_key_to_string(self):
        key = SecondaryLegislationKey(prefix="SR", year=2023, number=150)
        self.assertEqual(str(key), "SR 2023/150")

    def test_key_equality(self):
        k1 = SecondaryLegislationKey(prefix="SR", year=2023, number=150)
        k2 = SecondaryLegislationKey(prefix="SR", year=2023, number=150)
        k3 = SecondaryLegislationKey(prefix="LI", year=2024, number=56)
        self.assertEqual(k1, k2)
        self.assertNotEqual(k1, k3)

    def test_key_hashable(self):
        k1 = SecondaryLegislationKey(prefix="SR", year=2023, number=150)
        k2 = SecondaryLegislationKey(prefix="SR", year=2023, number=150)
        s = {k1, k2}
        self.assertEqual(len(s), 1)

    def test_key_to_dict(self):
        key = SecondaryLegislationKey(prefix="SR", year=2023, number=150)
        d = key.to_dict()
        self.assertEqual(d["prefix"], "SR")
        self.assertEqual(d["year"], 2023)
        self.assertEqual(d["number"], 150)
        self.assertEqual(d["key"], "SR 2023/150")

    def test_invalid_key_returns_none(self):
        self.assertIsNone(SecondaryLegislationKey.from_string(""))
        self.assertIsNone(SecondaryLegislationKey.from_string("Not a regulation"))
        self.assertIsNone(SecondaryLegislationKey.from_string("ABC"))
        self.assertIsNone(SecondaryLegislationKey.from_string("12345"))


class MapToLegislationKeyTest(unittest.TestCase):
    """Tests for map_to_legislation_key."""

    def test_maps_sr_to_key(self):
        key = map_to_legislation_key("SR 2023/150")
        self.assertIsNotNone(key)
        self.assertEqual(key.prefix, "SR")
        self.assertEqual(key.year, 2023)
        self.assertEqual(key.number, 150)

    def test_maps_li_to_key(self):
        key = map_to_legislation_key("LI 2024/56")
        self.assertIsNotNone(key)
        self.assertEqual(key.prefix, "LI")
        self.assertEqual(key.year, 2024)
        self.assertEqual(key.number, 56)

    def test_maps_named_regulation(self):
        key = map_to_legislation_key("ABC Regulations 2023")
        self.assertIsNotNone(key)
        self.assertEqual(key.year, 2023)

    def test_maps_statutory_instrument(self):
        key = map_to_legislation_key("SI 2024/33")
        self.assertIsNotNone(key)
        self.assertEqual(key.prefix, "SI")

    def test_returns_none_for_unparseable(self):
        self.assertIsNone(map_to_legislation_key(""))
        self.assertIsNone(map_to_legislation_key("Some random text"))
        self.assertIsNone(map_to_legislation_key(None))


class FakeResponse:
    """Minimal fake response for testing API calls."""

    def __init__(self, data: dict, status: int = 200):
        self._data = json.dumps(data).encode("utf-8")
        self.status = status
        self.offset = 0

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self, size: int = -1) -> bytes:
        if self.offset >= len(self._data):
            return b""
        if size < 0:
            size = len(self._data) - self.offset
        chunk = self._data[self.offset:self.offset + size]
        self.offset += len(chunk)
        return chunk

    def getcode(self) -> int:
        return self.status


class FakeOpener:
    """Fake urlopen replacement."""

    def __init__(self, data: dict, status: int = 200):
        self._data = data
        self._status = status
        self.captured_url: str | None = None

    def __call__(self, request):
        self.captured_url = str(request.full_url)
        return FakeResponse(self._data, self._status)


class LookupNzLegislationTest(unittest.TestCase):
    """Tests for lookup_nz_legislation."""

    def test_lookup_returns_legislation_data(self):
        api_response = {
            "title": "ABC Regulations 2023",
            "year": 2023,
            "type": "regulation",
            "status": "current",
            "url": "https://www.legislation.govt.nz/regulation/2023/0150",
        }
        opener = FakeOpener(api_response)
        key = SecondaryLegislationKey(prefix="SR", year=2023, number=150)
        result = lookup_nz_legislation(key, opener=opener)
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "ABC Regulations 2023")
        self.assertEqual(result["status"], "current")

    def test_lookup_constructs_correct_api_url(self):
        opener = FakeOpener({"title": "Test", "year": 2023})
        key = SecondaryLegislationKey(prefix="SR", year=2023, number=150)
        lookup_nz_legislation(key, opener=opener)
        self.assertIsNotNone(opener.captured_url)
        self.assertIn("regulation", opener.captured_url.lower())
        self.assertIn("2023", opener.captured_url)
        self.assertIn("0150", opener.captured_url)

    def test_lookup_handles_api_error(self):
        opener = FakeOpener({"error": "not_found"}, status=404)
        key = SecondaryLegislationKey(prefix="SR", year=1999, number=999)
        result = lookup_nz_legislation(key, opener=opener)
        self.assertIsNotNone(result)
        self.assertIn("error", result)

    def test_lookup_handles_network_error(self):
        def failing_opener(_request):
            raise OSError("Connection refused")
        key = SecondaryLegislationKey(prefix="SR", year=2023, number=150)
        result = lookup_nz_legislation(key, opener=failing_opener)
        self.assertIsNotNone(result)
        self.assertIn("error", result)

    def test_lookup_none_key_returns_none(self):
        self.assertIsNone(lookup_nz_legislation(None))


class BuildCorrelationIndexTest(unittest.TestCase):
    """Tests for build_correlation_index."""

    def test_build_index_from_complaints(self):
        complaints = [
            ComplaintRecord(
                subject="Complaint 2023/42",
                challenged_regulation="SR 2023/150",
                grounds="Ultra vires",
                recommendation="Revoke",
            ),
            ComplaintRecord(
                subject="Complaint 2024/15",
                challenged_regulation="LI 2024/56",
                grounds="Procedural defect",
                recommendation="Amend",
            ),
        ]
        index = build_correlation_index(complaints)
        self.assertEqual(len(index), 2)

    def test_index_contains_correlation_entries(self):
        complaints = [
            ComplaintRecord(
                subject="Complaint 2023/42",
                challenged_regulation="SR 2023/150",
            ),
        ]
        index = build_correlation_index(complaints)
        self.assertEqual(len(index), 1)
        entry = index[0]
        self.assertIsInstance(entry, CorrelationEntry)
        self.assertEqual(entry.complaint_subject, "Complaint 2023/42")
        self.assertIsNotNone(entry.legislation_key)

    def test_correlation_entry_skips_unparseable(self):
        complaints = [
            ComplaintRecord(
                subject="Complaint 2023/42",
                challenged_regulation=None,
            ),
        ]
        index = build_correlation_index(complaints)
        self.assertEqual(len(index), 0)

    def test_correlation_entry_with_api_result(self):
        api_result = {"title": "ABC Regulations 2023", "status": "current"}
        entry = CorrelationEntry(
            complaint_subject="Complaint 2023/42",
            legislation_key=SecondaryLegislationKey(prefix="SR", year=2023, number=150),
            api_result=api_result,
        )
        self.assertEqual(entry.complaint_subject, "Complaint 2023/42")
        self.assertEqual(entry.legislation_key.year, 2023)
        self.assertEqual(entry.api_result["title"], "ABC Regulations 2023")

    def test_correlation_entry_to_dict(self):
        entry = CorrelationEntry(
            complaint_subject="Complaint 2023/42",
            legislation_key=SecondaryLegislationKey(prefix="SR", year=2023, number=150),
        )
        d = entry.to_dict()
        self.assertEqual(d["complaint_subject"], "Complaint 2023/42")
        self.assertIn("legislation_key", d)
        self.assertEqual(d["legislation_key"]["key"], "SR 2023/150")

    def test_correlation_entry_to_dict_with_api(self):
        entry = CorrelationEntry(
            complaint_subject="Complaint 2023/42",
            legislation_key=SecondaryLegislationKey(prefix="SR", year=2023, number=150),
            api_result={"title": "ABC Regs", "status": "current"},
        )
        d = entry.to_dict()
        self.assertEqual(d["api_result"]["title"], "ABC Regs")


if __name__ == "__main__":
    unittest.main()
