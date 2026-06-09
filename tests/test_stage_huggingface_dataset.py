import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.stage_huggingface_dataset import stage_huggingface_dataset
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class StageHuggingFaceDatasetTest(unittest.TestCase):
    def test_stage_huggingface_dataset_copies_card_metadata_and_notice_files(self):
        case_dir = TEST_TMP / "stage_huggingface_dataset"
        project_dir = case_dir / "project"
        output_dir = case_dir / "out"
        parquet = project_dir / "generated" / "parquet" / "hansard.parquet"
        parquet.parent.mkdir(parents=True, exist_ok=True)
        parquet.write_bytes(b"parquet")

        for relative, content in {
            "DATASET_CARD.md": (
                "---\n"
                "license: mit\n"
                "configs:\n"
                "  - config_name: default\n"
                "    data_files:\n"
                "      - split: train\n"
                "        path: data/hansard.parquet\n"
                "---\n"
                "# Card"
            ),
            "README.md": "# Repo",
            "CITATION.cff": "doi: 10.5281/zenodo.20591997",
            "LICENSE": "MIT",
            "NOTICE.md": "notice",
            "VERSION": "0.1.0-review.test",
            "docs/report.md": "docs",
            "manifests/release.json": "{}",
            "schemas/schema.json": "{}",
        }.items():
            path = project_dir / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        cwd = Path.cwd()
        try:
            import os

            os.chdir(project_dir)
            result = stage_huggingface_dataset(output_dir=output_dir, parquet_path=parquet)
        finally:
            os.chdir(cwd)

        staged = Path(result["output_dir"])
        readme = (staged / "README.md").read_text(encoding="utf-8")
        self.assertTrue(readme.startswith("---"))
        self.assertIn("configs:", readme)
        self.assertIn("config_name: default", readme)
        self.assertIn("split: train", readme)
        self.assertIn("path: data/hansard.parquet", readme)
        self.assertTrue((staged / "CITATION.cff").exists())
        self.assertTrue((staged / "LICENSE").exists())
        self.assertTrue((staged / "NOTICE.md").exists())
        self.assertTrue((staged / "data" / "hansard.parquet").exists())
        self.assertTrue((staged / "manifests" / "release.json").exists())
        self.assertTrue((staged / "schemas" / "schema.json").exists())


if __name__ == "__main__":
    unittest.main()
