import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_release_package import build_release_package

TEST_TMP = Path(tempfile.gettempdir()) / "corpus-nz-hansard-tests"


class BuildReleasePackageTest(unittest.TestCase):
    def test_build_release_package_excludes_large_outputs_and_writes_checksums(self):
        case_dir = TEST_TMP / "release_package"
        project_dir = case_dir / "project"
        output_dir = case_dir / "out"
        project_dir.mkdir(parents=True, exist_ok=True)

        for relative, content in {
            "README.md": "readme",
            "CITATION.cff": "citation",
            "DATASET_CARD.md": "card",
            "LICENSE": "license",
            "NOTICE.md": "notice",
            "docs/report.md": "report",
            "manifests/source.json": "{}",
            "schemas/hansard_record.schema.json": "{}",
            "scripts/tool.py": "print('ok')",
            "tests/test_tool.py": "pass",
            "conductor/tracks.md": "# tracks",
            "VERSION": "0.1.0-review.test",
            "RELEASE_NOTES.md": "notes",
            "generated/parquet/hansard.parquet": "large",
            "source.zip": "source",
        }.items():
            path = project_dir / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        result = build_release_package(
            project_dir=project_dir,
            output_dir=output_dir,
            package_name="review.zip",
            source_archive_name="source.zip",
        )

        package_path = Path(result["package"])
        manifest_path = Path(result["manifest"])
        self.assertTrue(package_path.exists())
        self.assertTrue(manifest_path.exists())

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertIn("README.md", manifest["files"])
        self.assertIn("CITATION.cff", manifest["files"])
        self.assertIn("LICENSE", manifest["files"])
        self.assertIn("NOTICE.md", manifest["files"])
        self.assertIn("docs/report.md", manifest["files"])
        self.assertIn("schemas/hansard_record.schema.json", manifest["files"])
        self.assertNotIn("generated/parquet/hansard.parquet", manifest["files"])
        self.assertNotIn("source.zip", manifest["files"])

        with zipfile.ZipFile(package_path) as archive:
            names = set(archive.namelist())
        self.assertIn("README.md", names)
        self.assertIn("CITATION.cff", names)
        self.assertIn("LICENSE", names)
        self.assertIn("NOTICE.md", names)
        self.assertIn("schemas/hansard_record.schema.json", names)
        self.assertNotIn("generated/parquet/hansard.parquet", names)
        self.assertNotIn("source.zip", names)


if __name__ == "__main__":
    unittest.main()
