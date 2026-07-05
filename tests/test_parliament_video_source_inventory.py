from __future__ import annotations

import copy
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_parliament_video_source_inventory import (  # noqa: E402
    REQUIRED_ADJACENT_SOURCE_IDS,
    REQUIRED_FALLBACK_SOURCE_IDS,
    REQUIRED_OFFICIAL_SOURCE_IDS,
    REQUIRED_POLICY_FLAGS,
    _failures,
    _json,
    _validate_manifest,
)

MANIFEST_PATH = ROOT / "manifests/parliament_video_source_inventory.json"


class ParliamentVideoSourceInventoryTest(unittest.TestCase):
    def test_required_source_ids_are_present_by_role(self) -> None:
        manifest = _json(MANIFEST_PATH)
        sources = {source["source_id"]: source for source in manifest["sources"]}

        self.assertEqual(
            {
                source_id
                for source_id, source in sources.items()
                if source["source_role"] == "official"
            },
            REQUIRED_OFFICIAL_SOURCE_IDS,
        )
        self.assertEqual(
            {
                source_id
                for source_id, source in sources.items()
                if source["source_role"] == "fallback"
            },
            REQUIRED_FALLBACK_SOURCE_IDS,
        )
        self.assertEqual(
            {
                source_id
                for source_id, source in sources.items()
                if source["source_role"] == "supporting"
            },
            REQUIRED_ADJACENT_SOURCE_IDS,
        )

    def test_policy_forbids_media_downloads_and_completeness_claims(self) -> None:
        manifest = _json(MANIFEST_PATH)

        for flag in REQUIRED_POLICY_FLAGS:
            self.assertIs(manifest["policy"][flag], True)
        for source in manifest["sources"]:
            if source["source_role"] != "official":
                self.assertEqual(source["media_types"], ["metadata"])
            self.assertIn("no_media_download", source["acquisition_boundary"])
        self.assertEqual(
            {coverage["completion_claim"] for coverage in manifest["family_coverage"].values()},
            {"inventory-only-no-completeness-claim"},
        )

    def test_platform_sources_require_platform_terms_review(self) -> None:
        manifest = _json(MANIFEST_PATH)
        platform_sources = [
            source
            for source in manifest["sources"]
            if source["platform_class"] in {"youtube", "vimeo"}
        ]

        self.assertTrue(platform_sources)
        self.assertEqual(
            {source["rights_status"] for source in platform_sources},
            {"platform_terms_review_required"},
        )

    def test_checker_rejects_duplicate_source_ids(self) -> None:
        manifest = _json(MANIFEST_PATH)
        broken = copy.deepcopy(manifest)
        broken["sources"].append(copy.deepcopy(broken["sources"][0]))

        failures = _validate_manifest(broken)

        self.assertTrue(any("Duplicate source id" in failure for failure in failures))

    def test_checker_rejects_fallback_media_scope(self) -> None:
        manifest = _json(MANIFEST_PATH)
        broken = copy.deepcopy(manifest)
        for source in broken["sources"]:
            if source["source_role"] == "fallback":
                source["media_types"] = ["metadata", "video"]
                break

        failures = _validate_manifest(broken)

        self.assertTrue(
            any("fallback source must not list media downloads" in failure for failure in failures)
        )

    def test_checker_script_runs_successfully(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/check_parliament_video_source_inventory.py"],
            check=True,
            cwd=ROOT,
        )

    def test_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
