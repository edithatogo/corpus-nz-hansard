import sys
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.hf_private_source_archive import upload_source_archive
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class FakeHfApi:
    def __init__(self, token):
        self.token = token
        self.calls = []
        FakeHfApi.instances.append(self)

    instances = []

    def create_repo(self, **kwargs):
        self.calls.append(("create_repo", kwargs))

    def upload_file(self, **kwargs):
        self.calls.append(("upload_file", kwargs))


class HuggingFaceSourceArchiveTest(unittest.TestCase):
    def test_upload_source_archive_creates_private_dataset_and_returns_resolve_url(self):
        FakeHfApi.instances = []
        archive_path = TEST_TMP / f"source_{uuid.uuid4().hex}.zip"
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_bytes(b"archive")

        url = upload_source_archive(
            token="hf_test",
            repo_id="edithatogo/nz-hansard-source-archive",
            archive_path=archive_path,
            path_in_repo="source/test file.zip",
            api_factory=FakeHfApi,
        )

        api = FakeHfApi.instances[0]
        self.assertEqual(api.token, "hf_test")
        self.assertEqual(api.calls[0][0], "create_repo")
        self.assertTrue(api.calls[0][1]["private"])
        self.assertEqual(api.calls[1][0], "upload_file")
        self.assertEqual(api.calls[1][1]["path_in_repo"], "source/test file.zip")
        self.assertEqual(
            url,
            "https://huggingface.co/datasets/edithatogo/nz-hansard-source-archive/resolve/main/source/test%20file.zip",
        )


if __name__ == "__main__":
    unittest.main()
