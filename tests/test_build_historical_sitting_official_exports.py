import json
import sys
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from pypdf import PdfWriter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_historical_sitting_official_exports import (  # noqa: E402
    build_historical_sitting_official_exports,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


def _sample_pdf_bytes() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


class BuildHistoricalSittingOfficialExportsTest(unittest.TestCase):
    def test_build_official_exports_index_writes_json(self):
        case_dir = TEST_TMP / "historical_sitting_official_exports"
        case_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = case_dir / "manifest.json"
        output_path = case_dir / "official_export_index.json"
        cache_dir = case_dir / "pdf"

        manifest_path.write_text(
            json.dumps(
                {
                    "artifact_name": "historical_sitting_official_exports",
                    "artifact_version": "0.1.0",
                    "generated_at": "2026-06-13T00:00:00+00:00",
                    "repository": "corpus-nz-hansard",
                    "publication_stages": ["draft", "weekly", "sessional"],
                    "sources": [
                        {
                            "id": "sample-pdf",
                            "title": "Sample PDF",
                            "url": "https://example.com/sample.pdf",
                            "publication_stage": "weekly",
                            "coverage_note": "sample note",
                        }
                    ],
                    "authoritative_statements": [],
                    "notes": [],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        with patch(
            "scripts.build_historical_sitting_official_exports._download_pdf",
            return_value=_sample_pdf_bytes(),
        ):
            result = build_historical_sitting_official_exports(
                manifest_path=manifest_path,
                output_path=output_path,
                cache_dir=cache_dir,
            )

        self.assertTrue(output_path.exists())
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(result["artifact_name"], "historical_sitting_official_exports_index")
        self.assertEqual(len(payload["sources"]), 1)
        source = payload["sources"][0]
        self.assertEqual(source["id"], "sample-pdf")
        self.assertEqual(source["page_count"], 1)
        self.assertTrue(source["byte_size"] > 0)
        self.assertTrue((cache_dir / "sample-pdf.pdf").exists())


if __name__ == "__main__":
    unittest.main()
