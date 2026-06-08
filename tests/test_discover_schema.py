import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.discover_schema import build_schema_discovery, write_schema_discovery

TEST_TMP = Path(tempfile.gettempdir()) / "corpus-nz-hansard-tests"


class DiscoverSchemaTest(unittest.TestCase):
    def test_build_schema_discovery_detects_headers_rows_and_roles(self):
        case_dir = TEST_TMP / "schema_members"
        case_dir.mkdir(parents=True, exist_ok=True)
        archive_path = case_dir / "sample.zip"

        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            archive.writestr(
                "Hansard-1.csv",
                "SittingDate,Speaker,Party,SpeechText\n"
                "2024-01-01,Alice,LAB,Hello world\n"
                "2024-01-02,Bob,,Another speech\n",
            )
            archive.writestr(
                "Hansard-2.csv",
                "SittingDate,Speaker,Topic,SpeechText\n"
                "2024-01-03,Carol,Health,Third speech\n",
            )

        discovery = build_schema_discovery(archive_path, sample_rows=2)

        self.assertEqual(discovery["summary"]["file_count"], 2)
        self.assertEqual(discovery["summary"]["header_signatures"], 2)
        self.assertIn("Party", discovery["summary"]["all_columns"])
        self.assertIn("Topic", discovery["summary"]["all_columns"])

        first = discovery["files"][0]
        self.assertEqual(first["delimiter"], ",")
        self.assertEqual(first["row_count"], 2)
        self.assertEqual(first["headers"][0], "SittingDate")
        self.assertEqual(first["null_counts"]["Party"], 1)
        self.assertEqual(first["candidate_roles"]["date"], ["SittingDate"])
        self.assertEqual(first["candidate_roles"]["speaker"], ["Speaker"])
        self.assertEqual(first["candidate_roles"]["party"], ["Party"])
        self.assertEqual(first["candidate_roles"]["text"], ["SpeechText"])
        self.assertEqual(len(first["sample_rows"]), 2)

    def test_write_schema_discovery_creates_json_parent_directories(self):
        case_dir = TEST_TMP / "schema_write"
        case_dir.mkdir(parents=True, exist_ok=True)
        archive_path = case_dir / "sample.zip"
        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            archive.writestr("Hansard-1.csv", "A,B\n1,2\n")

        output_path = case_dir / "nested" / "schema_discovery.json"
        discovery = build_schema_discovery(archive_path, sample_rows=1)
        write_schema_discovery(discovery, output_path)

        self.assertTrue(output_path.exists())
        self.assertIn("Hansard-1.csv", output_path.read_text(encoding="utf-8"))

    def test_build_schema_discovery_allows_large_text_fields(self):
        case_dir = TEST_TMP / "schema_large_fields"
        case_dir.mkdir(parents=True, exist_ok=True)
        archive_path = case_dir / "sample.zip"
        large_text = "x" * 140_000

        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            archive.writestr("Hansard-1.csv", f"SpeechText\n{large_text}\n")

        discovery = build_schema_discovery(archive_path, sample_rows=1)

        self.assertEqual(discovery["files"][0]["row_count"], 1)
        self.assertEqual(discovery["files"][0]["sample_rows"][0]["SpeechText"], large_text)

    def test_build_schema_discovery_detects_utf16_headers(self):
        case_dir = TEST_TMP / "schema_utf16"
        case_dir.mkdir(parents=True, exist_ok=True)
        archive_path = case_dir / "sample.zip"
        payload = (
            "ParliamentNumber,DocumentContentDate,Content\n"
            "48,2024-01-01,Speech body\n"
        ).encode("utf-16")

        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            archive.writestr("Hansard-48.csv", payload)

        discovery = build_schema_discovery(archive_path, sample_rows=1)
        file_info = discovery["files"][0]

        self.assertEqual(file_info["encoding"], "utf-16")
        self.assertEqual(file_info["headers"], ["ParliamentNumber", "DocumentContentDate", "Content"])
        self.assertEqual(file_info["candidate_roles"]["date"], ["DocumentContentDate"])
        self.assertEqual(file_info["candidate_roles"]["text"], ["Content"])

    def test_build_schema_discovery_detects_utf16_le_without_bom(self):
        case_dir = TEST_TMP / "schema_utf16_le"
        case_dir.mkdir(parents=True, exist_ok=True)
        archive_path = case_dir / "sample.zip"
        payload = (
            "ParliamentNumber,DocumentContentDate,Content\n"
            "48,2024-01-01,Speech body\n"
        ).encode("utf-16-le")

        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            archive.writestr("Hansard-48.csv", payload)

        discovery = build_schema_discovery(archive_path, sample_rows=1)
        file_info = discovery["files"][0]

        self.assertEqual(file_info["encoding"], "utf-16-le")
        self.assertEqual(file_info["headers"], ["ParliamentNumber", "DocumentContentDate", "Content"])


if __name__ == "__main__":
    unittest.main()
