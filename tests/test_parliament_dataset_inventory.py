import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_parliament_dataset_inventory import (  # noqa: E402
    REQUIRED_DATASET_FAMILIES,
    _failures,
    _json,
    _validate_manifest,
)


MANIFEST_PATH = ROOT / "manifests/parliament_dataset_inventory.json"


class ParliamentDatasetInventoryTest(unittest.TestCase):
    def test_inventory_covers_required_dataset_families(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(set(manifest["dataset_families"]), REQUIRED_DATASET_FAMILIES)
        self.assertEqual(set(manifest["family_coverage"]), REQUIRED_DATASET_FAMILIES)

    def test_official_sources_precede_fallbacks_within_each_family(self):
        manifest = _json(MANIFEST_PATH)

        for family in REQUIRED_DATASET_FAMILIES:
            family_sources = [
                source
                for source in manifest["sources"]
                if family in source["dataset_families"] and source["source_posture"] != "excluded"
            ]
            first_non_official = next(
                (
                    index
                    for index, source in enumerate(family_sources)
                    if source["source_posture"] != "official"
                ),
                len(family_sources),
            )
            official_after_fallback = [
                source["id"]
                for source in family_sources[first_non_official:]
                if source["source_posture"] == "official"
            ]
            self.assertEqual(official_after_fallback, [], family)

    def test_exclusions_are_explicit_and_not_acquisition_sources(self):
        manifest = _json(MANIFEST_PATH)
        exclusions = {
            source["id"]: source
            for source in manifest["sources"]
            if source["source_posture"] == "excluded"
        }

        self.assertIn("excluded-nz-legislation", exclusions)
        self.assertIn("excluded-nz-gazette", exclusions)
        self.assertIn("excluded-hathitrust", exclusions)
        self.assertIn("excluded-internet-archive", exclusions)
        for source in exclusions.values():
            self.assertTrue(source["excluded"])
            self.assertEqual(source["acquisition_priority"], "excluded")

    def test_data_govt_requests_are_evidence_only(self):
        manifest = _json(MANIFEST_PATH)
        data_govt = [
            source for source in manifest["sources"] if source["publisher"] == "data.govt.nz"
        ]

        self.assertTrue(data_govt)
        self.assertTrue(all(source["source_posture"] == "evidence_only" for source in data_govt))
        self.assertTrue(
            all(source["acquisition_priority"] == "evidence_only" for source in data_govt)
        )

    def test_checker_rejects_duplicate_ids(self):
        manifest = _json(MANIFEST_PATH)
        broken = copy.deepcopy(manifest)
        broken["sources"].append(copy.deepcopy(broken["sources"][0]))

        failures = _validate_manifest(broken)

        self.assertTrue(any("Duplicate source id" in failure for failure in failures))

    def test_checker_rejects_fallback_without_relationship(self):
        manifest = _json(MANIFEST_PATH)
        broken = copy.deepcopy(manifest)
        for source in broken["sources"]:
            if source["source_posture"] == "fallback":
                source["fallback_for"] = []
                break

        failures = _validate_manifest(broken)

        self.assertTrue(any("fallback_for" in failure for failure in failures))

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
