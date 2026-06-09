import json
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.upload_zenodo_archive import upload_zenodo_archive

TEST_TMP = Path(tempfile.gettempdir()) / "corpus-nz-hansard-tests"


class FakeZenodoClient:
    def __init__(self):
        self.calls = []

    def ensure_draft(self, deposition_id=None, *, create_new_version=False):
        self.calls.append(("ensure_draft", deposition_id, create_new_version))
        return {"id": deposition_id or "draft-1", "links": {"bucket": "https://bucket.invalid"}}

    def upload_file(self, deposition, path):
        self.calls.append(("upload_file", deposition["id"], path.name))
        return {"filename": path.name}

    def delete_existing_files(self, deposition):
        self.calls.append(("delete_existing_files", deposition["id"]))

    def update_metadata(self, deposition_id, **kwargs):
        self.calls.append(("update_metadata", deposition_id, kwargs))
        return {"id": deposition_id, "metadata": kwargs}

class UploadZenodoArchiveTest(unittest.TestCase):
    def test_upload_zenodo_archive_updates_draft_without_publishing(self):
        case_dir = TEST_TMP / f"zenodo_upload_{uuid.uuid4().hex}"
        case_dir.mkdir(parents=True, exist_ok=True)
        archive_path = case_dir / "archive.tar.gz"
        manifest_path = case_dir / "archive.manifest.json"
        archive_path.write_bytes(b"archive")
        manifest_path.write_text(json.dumps({"ok": True}), encoding="utf-8")
        client = FakeZenodoClient()

        result = upload_zenodo_archive(
            archive_path=archive_path,
            manifest_path=manifest_path,
            token="token",
            creators=[{"name": "Maintainer"}],
            deposition_id="123",
            client=client,
        )

        self.assertEqual(result["deposition_id"], "123")
        self.assertFalse(result["published"])
        self.assertEqual(
            [call[0] for call in client.calls],
            [
                "ensure_draft",
                "delete_existing_files",
                "upload_file",
                "upload_file",
                "update_metadata",
            ],
        )

    def test_upload_zenodo_archive_can_create_new_version_without_publishing(self):
        case_dir = TEST_TMP / f"zenodo_publish_{uuid.uuid4().hex}"
        case_dir.mkdir(parents=True, exist_ok=True)
        archive_path = case_dir / "archive.tar.gz"
        manifest_path = case_dir / "archive.manifest.json"
        archive_path.write_bytes(b"archive")
        manifest_path.write_text(json.dumps({"ok": True}), encoding="utf-8")
        client = FakeZenodoClient()

        result = upload_zenodo_archive(
            archive_path=archive_path,
            manifest_path=manifest_path,
            token="token",
            creators=[{"name": "Maintainer"}],
            deposition_id="123",
            create_new_version=True,
            client=client,
        )

        self.assertFalse(result["published"])
        self.assertEqual(client.calls[0], ("ensure_draft", "123", True))
        self.assertEqual(client.calls[1], ("delete_existing_files", "123"))
        self.assertEqual(client.calls[-1][0], "update_metadata")


if __name__ == "__main__":
    unittest.main()
