import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_release_evidence_ledger import build_release_evidence_ledger
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class BuildReleaseEvidenceLedgerTest(unittest.TestCase):
    def test_builds_schema_valid_ledger_with_artifact_checksums(self):
        case_dir = TEST_TMP / "release_evidence_ledger"
        case_dir.mkdir(parents=True, exist_ok=True)
        manifest = case_dir / "release.manifest.json"
        artifact = case_dir / "release.tar.gz"
        output = case_dir / "ledger.json"
        manifest.write_text('{"manifest_version": 1}\n', encoding="utf-8")
        artifact.write_bytes(b"release artifact")

        ledger = build_release_evidence_ledger(
            output=output,
            repository="edithatogo/corpus-nz-hansard",
            commit_sha="a" * 40,
            workflow_name="Zenodo Archive Draft Package",
            workflow_run_id="123456",
            huggingface_repo_id="edithatogo/corpus-nz-hansard",
            huggingface_revision="abc123",
            zenodo_doi="10.5281/zenodo.1",
            zenodo_concept_doi="10.5281/zenodo.0",
            schema_version="1",
            record_count=10,
            coverage_statement="Document-level release.",
            manifests=(manifest,),
            artifacts=(artifact,),
        )

        self.assertTrue(output.exists())
        self.assertEqual(ledger["commit_sha"], "a" * 40)
        self.assertEqual(
            ledger["workflow"]["run_url"],
            "https://github.com/edithatogo/corpus-nz-hansard/actions/runs/123456",
        )
        self.assertEqual(ledger["dataset"]["record_count"], 10)
        self.assertEqual(ledger["manifests"][0]["bytes"], manifest.stat().st_size)
        self.assertEqual(ledger["artifacts"][0]["bytes"], artifact.stat().st_size)
        self.assertRegex(ledger["manifests"][0]["sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(ledger["artifacts"][0]["sha256"], r"^[0-9a-f]{64}$")

        strategies = {item["strategy"] for item in ledger["provenance_policy"]}
        self.assertIn("github_artifact_attestation", strategies)
        self.assertIn("revision_and_manifest_hash", strategies)
        self.assertIn("signed_checksum", strategies)
        self.assertIn("documented_deferral", strategies)

        schema = json.loads(
            (ROOT / "schemas/release_evidence_ledger.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator(schema).validate(ledger)


if __name__ == "__main__":
    unittest.main()
