import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.stage_huggingface_dataset import stage_huggingface_dataset

TEST_TMP = Path(tempfile.gettempdir()) / "corpus-nz-hansard-tests"


class StageHuggingFaceDatasetTest(unittest.TestCase):
    def test_stage_huggingface_dataset_copies_card_metadata_and_notice_files(self):
        case_dir = TEST_TMP / "stage_huggingface_dataset"
        project_dir = case_dir / "project"
        output_dir = case_dir / "out"
        parquet = project_dir / "generated" / "parquet" / "hansard.parquet"
        parquet.parent.mkdir(parents=True, exist_ok=True)
        parquet.write_bytes(b"parquet")

        for relative, content in {
            "DATASET_CARD.md": "---\nlicense: mit\n---\n# Card",
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
        self.assertTrue((staged / "README.md").read_text(encoding="utf-8").startswith("---"))
        self.assertTrue((staged / "CITATION.cff").exists())
        self.assertTrue((staged / "LICENSE").exists())
        self.assertTrue((staged / "NOTICE.md").exists())
        self.assertTrue((staged / "data" / "hansard.parquet").exists())


if __name__ == "__main__":
    unittest.main()
