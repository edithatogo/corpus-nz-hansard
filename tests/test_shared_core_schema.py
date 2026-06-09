import json
import sys
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_shared_core_schema import _failures


def _validator() -> Any:
    schema_path = ROOT / "schemas/shared_nz_corpus_core.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def _valid_record(corpus_id: str = "corpus-nz-hansard") -> dict[str, Any]:
    return {
        "corpus_id": corpus_id,
        "record_id": "nz-hansard-1854-000001",
        "source_id": "documentsdb:hansard:1854:000001",
        "jurisdiction": "New Zealand",
        "country": "NZ",
        "document_type": "hansard_document",
        "record_schema_version": "v1",
        "canonical_uri": "https://example.org/corpus-nz-hansard/records/nz-hansard-1854-000001",
        "source_url": "https://www.parliament.nz/en/pb/hansard-debates/",
        "source_version": "documentsdb-2026-06-08",
        "effective_date": "1854-05-24",
        "published_date": "1854-05-24",
        "last_modified_date": None,
        "content_sha256": "a" * 64,
        "manifest_sha256": "b" * 64,
        "provenance": {
            "pipeline_name": "corpus-nz-hansard",
            "pipeline_version": "0.1.0",
            "source_name": "New Zealand Parliamentary Debates/Hansard",
            "source_record_id": "documentsdb:hansard:1854:000001",
            "source_retrieved_at": None,
            "release_version": "0.1.0",
            "release_commit": "3551391",
            "license_note": "Hansard source-text provenance is documented in release metadata.",
        },
    }


class SharedCoreSchemaTest(unittest.TestCase):
    def test_valid_hansard_core_record_passes(self):
        _validator().validate(_valid_record())

    def test_valid_legislation_core_record_passes(self):
        record = _valid_record("corpus-nz-legislation")
        record["record_id"] = "nz-legislation-act-1908-000001"
        record["source_id"] = "nzlii:act:1908:000001"
        record["document_type"] = "act"
        record["canonical_uri"] = (
            "https://example.org/corpus-nz-legislation/records/nz-legislation-act-1908-000001"
        )
        record["source_url"] = "https://www.legislation.govt.nz/"
        record["provenance"]["pipeline_name"] = "corpus-nz-legislation"
        record["provenance"]["source_name"] = "New Zealand Legislation"
        record["provenance"]["source_record_id"] = "nzlii:act:1908:000001"

        _validator().validate(record)

    def test_rejects_wrong_corpus_label(self):
        record = _valid_record("nz-hansard")
        errors = list(_validator().iter_errors(record))

        self.assertTrue(any(error.path and error.path[0] == "corpus_id" for error in errors))

    def test_rejects_missing_manifest_hash(self):
        record = _valid_record()
        del record["manifest_sha256"]
        errors = list(_validator().iter_errors(record))

        self.assertTrue(any("manifest_sha256" in error.message for error in errors))

    def test_repository_shared_core_contract_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
