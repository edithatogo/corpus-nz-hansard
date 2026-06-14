"""Tests for download caching and incremental update logic."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.select_committee_reports.cache import (
    CacheManifest,
    load_manifest,
    save_manifest,
    is_cached,
    mark_cached,
    compute_file_hash,
    get_stale_entries,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class CacheManifestTest(unittest.TestCase):

    def test_manifest_defaults(self):
        m = CacheManifest()
        self.assertEqual(m.version, 1)
        self.assertEqual(m.entries, {})

    def test_manifest_add_entry(self):
        m = CacheManifest()
        m.entries["rep-001"] = {
            "url": "https://example.com/report.pdf",
            "sha256": "abc123",
            "size": 1024,
            "format": "pdf",
            "cached_at": "2024-06-30T12:00:00",
        }
        self.assertIn("rep-001", m.entries)


class LoadSaveManifestTest(unittest.TestCase):

    def setUp(self):
        self.manifest_path = TEST_TMP / "cache_manifest.json"
        if self.manifest_path.exists():
            self.manifest_path.unlink()

    def tearDown(self):
        if self.manifest_path.exists():
            self.manifest_path.unlink()

    def test_save_and_load_manifest(self):
        m = CacheManifest()
        m.entries["rep-001"] = {
            "url": "https://example.com/report.pdf",
            "sha256": "def456",
            "size": 2048,
            "format": "pdf",
            "cached_at": "2024-07-01T00:00:00",
        }
        save_manifest(m, self.manifest_path)
        self.assertTrue(self.manifest_path.exists())

        loaded = load_manifest(self.manifest_path)
        self.assertEqual(loaded.version, 1)
        self.assertIn("rep-001", loaded.entries)
        self.assertEqual(loaded.entries["rep-001"]["sha256"], "def456")

    def test_load_nonexistent_manifest(self):
        m = load_manifest(TEST_TMP / "nonexistent.json")
        self.assertIsInstance(m, CacheManifest)
        self.assertEqual(m.entries, {})

    def test_load_corrupt_manifest(self):
        bad_path = TEST_TMP / "corrupt_manifest.json"
        bad_path.write_text("not valid json", encoding="utf-8")
        m = load_manifest(bad_path)
        self.assertIsInstance(m, CacheManifest)
        self.assertEqual(m.entries, {})


class IsCachedTest(unittest.TestCase):

    def setUp(self):
        self.manifest_path = TEST_TMP / "cache_check.json"

    def tearDown(self):
        if self.manifest_path.exists():
            self.manifest_path.unlink()

    def test_entry_not_cached(self):
        m = CacheManifest()
        self.assertFalse(is_cached(m, "rep-none"))

    def test_entry_is_cached(self):
        m = CacheManifest()
        m.entries["rep-001"] = {
            "url": "https://example.com/r.pdf",
            "sha256": "abc",
            "size": 100,
            "format": "pdf",
            "cached_at": "2024-01-01T00:00:00",
        }
        self.assertTrue(is_cached(m, "rep-001"))


class MarkCachedTest(unittest.TestCase):

    def test_mark_cached_adds_entry(self):
        m = CacheManifest()
        mark_cached(m, "rep-001", url="https://example.com/r.pdf", file_hash="xyz", size=500, fmt="pdf")
        self.assertIn("rep-001", m.entries)
        self.assertEqual(m.entries["rep-001"]["sha256"], "xyz")
        self.assertIn("cached_at", m.entries["rep-001"])
        self.assertEqual(m.entries["rep-001"]["format"], "pdf")


class ComputeFileHashTest(unittest.TestCase):

    def test_compute_hash_of_file(self):
        f = TEST_TMP / "hash_me.txt"
        f.write_text("hello world", encoding="utf-8")
        h = compute_file_hash(f)
        self.assertEqual(len(h), 64)  # SHA-256 hex length
        self.assertTrue(all(c in "0123456789abcdef" for c in h))

    def test_compute_hash_nonexistent(self):
        h = compute_file_hash(TEST_TMP / "no_such_file.bin")
        self.assertEqual(h, "")


class GetStaleEntriesTest(unittest.TestCase):

    def test_no_stale_entries(self):
        m = CacheManifest()
        m.entries["rep-current"] = {
            "sha256": "abc",
            "cached_at": "2024-12-01T00:00:00",
        }
        stale = get_stale_entries(m, max_age_days=30, reference_date="2024-12-15")
        self.assertEqual(stale, [])

    def test_stale_entry(self):
        m = CacheManifest()
        m.entries["rep-old"] = {
            "sha256": "abc",
            "cached_at": "2024-01-01T00:00:00",
        }
        stale = get_stale_entries(m, max_age_days=30, reference_date="2024-12-15")
        self.assertEqual(stale, ["rep-old"])

    def test_stale_entry_no_cached_at(self):
        m = CacheManifest()
        m.entries["rep-no-date"] = {"sha256": "abc"}
        stale = get_stale_entries(m, max_age_days=30, reference_date="2024-12-15")
        self.assertEqual(stale, [])


if __name__ == "__main__":
    unittest.main()
