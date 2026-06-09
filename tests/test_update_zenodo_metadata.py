import sys
import unittest
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.update_zenodo_metadata import (
    ZenodoMetadataClient,
    merge_related_identifiers,
    update_zenodo_metadata,
)


class FakeZenodoMetadataClient:
    def __init__(self):
        self.calls = []

    def get_deposition(self, deposition_id):
        self.calls.append(("get_deposition", deposition_id))
        return {
            "id": deposition_id,
            "submitted": True,
            "metadata": {
                "title": "NZ Hansard Corpus",
                "upload_type": "dataset",
                "description": "old",
                "creators": [{"name": "Maintainer"}],
                "version": "0.1.0",
                "related_identifiers": [
                    {
                        "identifier": "https://doi.org/10.5281/zenodo.20595194",
                        "relation": "isVersionOf",
                        "scheme": "doi",
                    }
                ],
            },
        }

    def edit_deposition(self, deposition_id):
        self.calls.append(("edit_deposition", deposition_id))
        return {
            "id": deposition_id,
            "submitted": False,
            "metadata": {
                "title": "NZ Hansard Corpus",
                "upload_type": "dataset",
                "description": "old",
                "creators": [{"name": "Maintainer"}],
                "version": "0.1.0",
                "related_identifiers": [
                    {
                        "identifier": "https://doi.org/10.5281/zenodo.20595194",
                        "relation": "isVersionOf",
                        "scheme": "doi",
                    }
                ],
            },
        }

    def put_metadata(self, deposition_id, metadata):
        self.calls.append(("put_metadata", deposition_id, metadata))
        return {"id": deposition_id, "metadata": metadata}

    def publish(self, deposition_id):
        self.calls.append(("publish", deposition_id))
        return {"id": deposition_id, "submitted": True}


class UpdateZenodoMetadataTest(unittest.TestCase):
    def test_update_zenodo_metadata_adds_cross_references_and_publishes(self):
        client = FakeZenodoMetadataClient()

        result = update_zenodo_metadata(
            deposition_id="20595194",
            token="token",
            client=client,
        )

        self.assertTrue(result["published"])
        self.assertEqual(
            [call[0] for call in client.calls],
            ["get_deposition", "edit_deposition", "put_metadata", "publish"],
        )
        metadata = client.calls[2][2]
        identifiers = metadata["related_identifiers"]
        self.assertIn(
            "https://github.com/edithatogo/corpus-nz-hansard",
            [item["identifier"] for item in identifiers],
        )
        self.assertIn(
            "https://huggingface.co/datasets/edithatogo/nz-hansard-corpus",
            [item["identifier"] for item in identifiers],
        )
        self.assertIn(
            "https://doi.org/10.5281/zenodo.20595194",
            [item["identifier"] for item in identifiers],
        )
        self.assertIn("Public surfaces:", metadata["description"])

    def test_update_zenodo_metadata_can_skip_publish(self):
        client = FakeZenodoMetadataClient()

        result = update_zenodo_metadata(
            deposition_id="20595194",
            token="token",
            client=client,
            publish=False,
        )

        self.assertFalse(result["published"])
        self.assertNotIn("publish", [call[0] for call in client.calls])

    def test_merge_related_identifiers_preserves_and_updates_existing_items(self):
        merged = merge_related_identifiers(
            [
                {
                    "identifier": "https://example.invalid/original",
                    "relation": "isSupplementedBy",
                    "scheme": "url",
                },
                {
                    "identifier": "https://github.com/edithatogo/corpus-nz-hansard",
                    "relation": "isSupplementTo",
                    "scheme": "url",
                },
            ]
        )

        identifiers = [item["identifier"] for item in merged]
        self.assertIn("https://example.invalid/original", identifiers)
        github = next(
            item
            for item in merged
            if item["identifier"] == "https://github.com/edithatogo/corpus-nz-hansard"
        )
        self.assertEqual(github["relation"], "isSupplementedBy")

    def test_client_retries_transient_server_errors(self):
        class FakeResponse:
            def __init__(self, status_code, body):
                self.status_code = status_code
                self.text = body

            def raise_for_status(self):
                if self.status_code >= 400:
                    raise requests.HTTPError(f"{self.status_code} error", response=self)

            def json(self):
                return {"ok": True}

        class FakeSession:
            def __init__(self):
                self.calls = 0

            def request(self, method, url, **kwargs):
                self.calls += 1
                if self.calls == 1:
                    return FakeResponse(504, "timeout")
                return FakeResponse(200, "{}")

        session = FakeSession()
        client = ZenodoMetadataClient(
            api_url="https://zenodo.example/api",
            token="token",
            session=session,
            max_retries=1,
            retry_sleep=0,
        )

        self.assertEqual(client.request("GET", "https://zenodo.example/api/test"), {"ok": True})
        self.assertEqual(session.calls, 2)


if __name__ == "__main__":
    unittest.main()
