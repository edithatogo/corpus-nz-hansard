import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_zenodo_archive import build_zenodo_archive

TEST_TMP = Path(tempfile.gettempdir()) / "corpus-nz-hansard-tests"


class BuildZenodoArchiveTest(unittest.TestCase):
    def test_build_zenodo_archive_includes_license_and_notice(self):
        case_dir = TEST_TMP / "build_zenodo_archive"
        project_dir = case_dir / "project"
        output_dir = case_dir / "out"
        parquet = project_dir / "generated" / "parquet" / "hansard.parquet"
        parquet.parent.mkdir(parents=True, exist_ok=True)
        parquet.write_bytes(b"parquet")

        for relative, content in {
            "CITATION.cff": "citation",
            "DATASET_CARD.md": "card",
            "LICENSE": "license",
            "NOTICE.md": "notice",
            "README.md": "readme",
            "RELEASE_NOTES.md": "notes",
            "VERSION": "0.1.0-review.test",
            "requirements.txt": "duckdb",
        }.items():
            path = project_dir / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        cwd = Path.cwd()
        try:
            import os

            os.chdir(project_dir)
            result = build_zenodo_archive(
                output_dir=output_dir,
                version="0.1.0-review.test",
                parquet_path=parquet,
            )
        finally:
            os.chdir(cwd)

        with tarfile.open(result["archive"], "r:gz") as archive:
            names = set(archive.getnames())

        root = "nz-hansard-corpus-0.1.0-review.test"
        self.assertIn(f"{root}/LICENSE", names)
        self.assertIn(f"{root}/NOTICE.md", names)
        self.assertIn(f"{root}/data/hansard.parquet", names)


if __name__ == "__main__":
    unittest.main()
