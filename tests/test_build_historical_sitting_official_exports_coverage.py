import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_historical_sitting_official_exports_coverage import (  # noqa: E402
    build_historical_sitting_official_exports_coverage,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class BuildHistoricalSittingOfficialExportsCoverageTest(unittest.TestCase):
    def test_build_official_exports_coverage_writes_report(self):
        output_path = TEST_TMP / "historical_sitting_official_exports_coverage.json"

        def fake_extract_pdf_dates(pdf_path: Path) -> list[str]:
            if "49th" in pdf_path.name:
                return ["Tuesday, 20 July 2010", "Tuesday, 27 July 2010"]
            if "51st" in pdf_path.name:
                return ["Tuesday, 20 July 2010", "Wednesday, 21 July 2011"]
            return ["Wednesday, 21 July 2010", "Thursday, 22 July 2011"]

        with patch(
            "scripts.build_historical_sitting_official_exports_coverage._extract_pdf_dates",
            side_effect=fake_extract_pdf_dates,
        ), patch(
            "scripts.build_historical_sitting_official_exports_coverage._load_ledger_dates",
            return_value={"2010-07-20", "2011-07-21"},
        ):
            result = build_historical_sitting_official_exports_coverage(output_path=output_path)

        self.assertTrue(output_path.exists())
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(result["artifact_name"], "historical_sitting_official_exports_coverage")
        self.assertEqual(payload["shared_date_count"], 2)
        self.assertEqual(payload["official_date_count"], 5)
        self.assertEqual(payload["ledger_date_count"], 2)
        self.assertEqual(payload["official_years"], ["2010", "2011"])
        self.assertEqual(payload["ledger_years"], ["2010", "2011"])
        self.assertGreaterEqual(len(payload["year_summary"]), 1)
        self.assertEqual(payload["acquisition_priority_years"], [])
        self.assertIn("status", payload["year_summary"][0])
        self.assertEqual(len(payload["sources"]), 3)
        self.assertTrue(payload["sources"][0]["shared_dates_with_ledger"] >= 1)


if __name__ == "__main__":
    unittest.main()
