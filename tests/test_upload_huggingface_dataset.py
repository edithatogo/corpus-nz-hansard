import json
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.upload_huggingface_dataset import upload_huggingface_dataset
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class FakeHfApi:
    def __init__(self):
        self.calls = []

    def create_repo(self, **kwargs):
        self.calls.append(("create_repo", kwargs))
        return {"url": "https://huggingface.co/datasets/example/repo"}

    def update_repo_settings(self, **kwargs):
        self.calls.append(("update_repo_settings", kwargs))
        return None

    def upload_folder(self, **kwargs):
        self.calls.append(("upload_folder", kwargs))
        return {"commit": "abc"}


class UploadHuggingFaceDatasetTest(unittest.TestCase):
    def test_upload_huggingface_dataset_creates_repo_and_uploads_folder(self):
        case_dir = TEST_TMP / f"hf_upload_{uuid.uuid4().hex}"
        folder = case_dir / "huggingface"
        (folder / "data").mkdir(parents=True)
        (folder / "manifests").mkdir()
        (folder / "data" / "hansard.parquet").write_bytes(b"parquet")
        (folder / "manifests" / "public_dataset_release_manifest.json").write_text(
            json.dumps({"published": False}),
            encoding="utf-8",
        )
        api = FakeHfApi()

        result = upload_huggingface_dataset(
            repo_id="example/repo",
            folder=folder,
            token="token",
            api=api,
        )

        self.assertTrue(result["uploaded"])
        self.assertFalse(result["gated"])
        self.assertEqual(
            [call[0] for call in api.calls],
            ["create_repo", "update_repo_settings", "upload_folder"],
        )
        self.assertEqual(api.calls[0][1]["repo_type"], "dataset")
        self.assertEqual(api.calls[1][1]["repo_type"], "dataset")
        self.assertFalse(api.calls[1][1]["gated"])
        self.assertFalse(api.calls[1][1]["private"])
        self.assertEqual(api.calls[2][1]["path_in_repo"], ".")

    def test_upload_huggingface_dataset_requires_staged_parquet(self):
        case_dir = TEST_TMP / f"hf_missing_{uuid.uuid4().hex}"
        folder = case_dir / "huggingface"
        folder.mkdir(parents=True)

        with self.assertRaises(FileNotFoundError):
            upload_huggingface_dataset(
                repo_id="example/repo",
                folder=folder,
                token="token",
                api=FakeHfApi(),
            )


if __name__ == "__main__":
    unittest.main()
