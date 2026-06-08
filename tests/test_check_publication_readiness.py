import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_publication_readiness import check_publication_readiness, format_results


class PublicationReadinessTest(unittest.TestCase):
    def test_huggingface_requires_token_and_source_url(self):
        results = check_publication_readiness(env={}, targets=("huggingface",))

        self.assertEqual([result.name for result in results], ["HF_TOKEN", "SOURCE_ARCHIVE_URL"])
        self.assertFalse(all(result.ready for result in results))

    def test_huggingface_ready_when_required_values_present(self):
        results = check_publication_readiness(
            env={
                "HF_TOKEN": "hf_test",
                "SOURCE_ARCHIVE_URL": "https://example.invalid/source.zip",
            },
            targets=("huggingface",),
        )

        self.assertTrue(all(result.ready for result in results))

    def test_zenodo_requires_token_source_url_and_creator_metadata(self):
        results = check_publication_readiness(env={}, targets=("zenodo",))

        self.assertEqual(
            [result.name for result in results],
            ["ZENODO_TOKEN", "SOURCE_ARCHIVE_URL", "HF_TOKEN", "ARCHIVE_CREATORS_JSON"],
        )
        self.assertFalse(all(result.ready for result in results))

    def test_zenodo_rejects_invalid_creator_metadata(self):
        results = check_publication_readiness(
            env={
                "ZENODO_TOKEN": "token",
                "SOURCE_ARCHIVE_URL": "https://example.invalid/source.zip",
                "HF_TOKEN": "hf_test",
                "ARCHIVE_CREATORS_JSON": '[{"orcid":"0000"}]',
            },
            targets=("zenodo",),
        )

        creator_result = results[-1]
        self.assertEqual(creator_result.name, "ARCHIVE_CREATORS_JSON")
        self.assertFalse(creator_result.ready)
        self.assertIn("non-empty name", creator_result.detail)

    def test_format_results_does_not_print_secret_values(self):
        results = check_publication_readiness(
            env={
                "HF_TOKEN": "hf_secret_value",
                "SOURCE_ARCHIVE_URL": "https://example.invalid/source.zip",
            },
            targets=("huggingface",),
        )

        output = format_results(results)
        self.assertIn("[READY] huggingface: HF_TOKEN", output)
        self.assertNotIn("hf_secret_value", output)
        self.assertNotIn("https://example.invalid/source.zip", output)


if __name__ == "__main__":
    unittest.main()
