import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.publish_zenodo_deposition import publish_zenodo_deposition


class FakeZenodoPublishClient:
    def __init__(self):
        self.calls = []

    def publish(self, deposition_id):
        self.calls.append(("publish", deposition_id))
        return {"id": deposition_id, "submitted": True}


class PublishZenodoDepositionTest(unittest.TestCase):
    def test_publish_zenodo_deposition_uses_explicit_publish_client(self):
        client = FakeZenodoPublishClient()

        result = publish_zenodo_deposition(
            deposition_id="draft-123",
            token="token",
            client=client,
        )

        self.assertTrue(result["published"])
        self.assertEqual(result["deposition_id"], "draft-123")
        self.assertEqual(client.calls, [("publish", "draft-123")])


if __name__ == "__main__":
    unittest.main()
