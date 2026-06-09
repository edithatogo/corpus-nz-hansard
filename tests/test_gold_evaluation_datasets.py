import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_gold_evaluation_datasets import (
    FIXTURE_PATH,
    REQUIRED_CLASSES,
    REQUIRED_DOMAINS,
    _failures,
    _json,
)


class GoldEvaluationDatasetsTest(unittest.TestCase):
    def test_fixture_covers_each_domain_and_class(self):
        fixtures = _json(FIXTURE_PATH)
        classes_by_domain = {domain: set() for domain in REQUIRED_DOMAINS}
        for sample in fixtures["samples"]:
            classes_by_domain[sample["domain"]].add(sample["example_class"])

        self.assertEqual(set(classes_by_domain), REQUIRED_DOMAINS)
        for classes in classes_by_domain.values():
            self.assertEqual(classes, REQUIRED_CLASSES)

    def test_all_samples_are_reviewed_not_model_gold(self):
        fixtures = _json(FIXTURE_PATH)

        self.assertTrue(fixtures["samples"])
        for sample in fixtures["samples"]:
            self.assertEqual(sample["review"]["review_status"], "reviewed")
            self.assertFalse(sample["review"]["model_generated_label"])
            self.assertTrue(sample["label"]["label_provenance"])

    def test_each_sample_references_document_release(self):
        fixtures = _json(FIXTURE_PATH)

        self.assertEqual(
            {sample["source_reference"]["release_version"] for sample in fixtures["samples"]},
            {"0.1.0"},
        )

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
