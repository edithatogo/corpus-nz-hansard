import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_historical_sitting_weekly_archive_index import (  # noqa: E402
    build_historical_sitting_weekly_archive_index,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class BuildHistoricalSittingWeeklyArchiveIndexTest(unittest.TestCase):
    def test_build_weekly_archive_index_writes_report(self):
        output_path = TEST_TMP / "weekly_journals_archive_index.json"
        page_reports = [
            {
                "page_number": 23,
                "articles": [
                    {
                        "article_url": "https://example.test/a",
                        "title": "Journals of the House for the week beginning Tuesday, 17 July 2007",
                        "pdf_href": "https://example.test/a.pdf",
                    },
                    {
                        "article_url": "https://example.test/b",
                        "title": "Journals of the House for the week beginning Tuesday, 12 December 2006",
                        "pdf_href": "https://example.test/b.pdf",
                    },
                ],
            }
        ]

        result = build_historical_sitting_weekly_archive_index(
            page_reports=page_reports,
            output_path=output_path,
            generated_at="2026-06-13T00:00:00+00:00",
        )

        self.assertTrue(output_path.exists())
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(result["artifact_name"], "historical_sitting_weekly_archive_index")
        self.assertEqual(payload["summary"]["pages_crawled"], 1)
        self.assertEqual(payload["summary"]["article_count"], 2)
        self.assertEqual(payload["summary"]["pdf_href_count"], 2)
        self.assertEqual(payload["summary"]["year_coverage"], ["2006", "2007"])
        self.assertEqual(payload["pages"][0]["first_title"], "Journals of the House for the week beginning Tuesday, 17 July 2007")
        self.assertEqual(payload["pages"][0]["last_title"], "Journals of the House for the week beginning Tuesday, 12 December 2006")
        self.assertEqual(len(payload["notes"]), 3)


if __name__ == "__main__":
    unittest.main()
