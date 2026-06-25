from __future__ import annotations

import json
import unittest

from scripts.check_multi_git_archive_mirroring import (
    APPROVED_CHECKOUT_SHA,
    QUALITY_WORKFLOW_PATH,
    STATUS_MANIFEST_PATH,
    WORKFLOW_PATH,
    _failures,
)


class MultiGitArchiveMirroringTests(unittest.TestCase):
    def test_mirror_workflow_has_expected_triggers_and_pinned_checkout(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("push:", workflow)
        self.assertIn("branches: [ main, master ]", workflow)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn(f"actions/checkout@{APPROVED_CHECKOUT_SHA}", workflow)

    def test_mirror_workflow_skips_without_complete_secret_pair(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn('if [ -z "$GIT_MIRROR_URL" ]; then', workflow)
        self.assertIn('if [ -z "$GIT_MIRROR_SSH_PRIVATE_KEY" ]; then', workflow)
        self.assertIn("GIT_MIRROR_URL: ${{ secrets.GIT_MIRROR_URL }}", workflow)
        self.assertIn(
            "GIT_MIRROR_SSH_PRIVATE_KEY: ${{ secrets.GIT_MIRROR_SSH_PRIVATE_KEY }}",
            workflow,
        )

    def test_quality_runs_osf_policy_before_mirror_linkage_check(self) -> None:
        workflow = QUALITY_WORKFLOW_PATH.read_text(encoding="utf-8")

        osf_check = workflow.find("check_osf_optional_mirror_policy.py")
        mirror_check = workflow.find("check_multi_git_archive_mirroring.py")

        self.assertGreaterEqual(osf_check, 0)
        self.assertGreater(mirror_check, osf_check)

    def test_status_manifest_records_repo_side_readiness_and_live_blocker(self) -> None:
        manifest = json.loads(STATUS_MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(manifest["repo_side_status"], "implemented")
        self.assertEqual(
            manifest["live_status"],
            "deferred-to-future-roadmap",
        )
        self.assertEqual(
            manifest["workflow"]["incomplete_secret_pair_behavior"],
            "skip-before-ssh-setup",
        )
        self.assertFalse(manifest["archives"]["osf_claims_allowed"])
        self.assertIn("edithatogo", " ".join(manifest["blocked_on"]))
        self.assertEqual(manifest["future_roadmap_ref"], "conductor/improvement-backlog.md")
        self.assertIn("GIT_MIRROR_URL", " ".join(manifest["blocked_on"]))
        self.assertIn("GIT_MIRROR_SSH_PRIVATE_KEY", " ".join(manifest["blocked_on"]))
        self.assertIn("Mirror Sync", " ".join(manifest["blocked_on"]))

    def test_repo_side_multi_git_archive_contract_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
