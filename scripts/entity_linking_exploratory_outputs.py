"""Seed data and helpers for exploratory entity linking outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "samples/entity-linking-exploratory"
JSONL_PATH = SAMPLE_DIR / "entity_linking_exploratory.jsonl"
REVIEW_PATH = SAMPLE_DIR / "entity_linking_exploratory_review.csv"
README_PATH = SAMPLE_DIR / "README.md"
DOC_PATH = ROOT / "docs/entity-linking-exploratory-outputs.md"
MANIFEST_PATH = ROOT / "manifests/entity_linking_exploratory_outputs.json"
SCHEMA_PATH = ROOT / "schemas/entity_linking_exploratory_outputs.schema.json"
RECORD_SCHEMA_PATH = ROOT / "schemas/entity_linking_exploratory_record.schema.json"

AUTHORITY_SOURCE_URLS = {
    "nz-parliament-members-current": "https://www3.parliament.nz/en/mps-and-electorates/members-of-parliament/",
    "nz-parliament-parties-current": "https://www3.parliament.nz/en/mps-and-electorates/political-parties/",
    "nz-parliament-bills-current": "https://bills.parliament.nz/bills-proposed-laws?Tab=Current&lang=en",
    "nz-parliament-order-paper": "https://www3.parliament.nz/en/pb/order-paper-questions/order-paper",
    "nz-parliament-hansard-current": "https://hansard.parliament.nz/hansard-debates/rhr?lang=en",
    "nz-parliament-daily-progress": "https://www3.parliament.nz/en/pb/daily-progress-in-the-house",
    "nz-parliament-parliamentary-rules": "https://www3.parliament.nz/en/pb/parliamentary-rules/",
}

ENTITY_LINKING_ROWS: list[dict[str, Any]] = [
    {
        "record_id": "entity-linking-01",
        "entity_type": "person",
        "example_class": "ambiguous",
        "mention_text": "Megan Woods",
        "source_document_type": "Hansard - speech",
        "parliament_number": 47,
        "source_stable_id": "47HansS_20240625_067140000",
        "source_excerpt": "Hon Dr MEGAN WOODS (Labour-Wigram): Thank you Mr Speaker.",
        "selector": {
            "selector_type": "exact",
            "exact": "MEGAN WOODS",
            "source_stable_id": "47HansS_20240625_067140000",
        },
        "candidate_links": [
            {
                "candidate_id": None,
                "candidate_label": "Megan Woods",
                "candidate_uri": None,
                "authority_source_id": "nz-parliament-members-current",
                "authority_source_url": AUTHORITY_SOURCE_URLS["nz-parliament-members-current"],
                "score": 0.62,
                "match_method": "honorific-plus-name",
                "linking_status": "ambiguous",
            }
        ],
        "linking_status": "ambiguous",
        "provenance": {
            "method": "rule-plus-authority-source",
            "rule_bundle": "entity-linking-exploratory-rules-v0.1",
            "authority_sources": ["nz-parliament-members-current"],
            "human_validation": False,
        },
        "validation_status": "exploratory-only",
        "review_status": "reviewed",
        "release_status": "sample-not-release",
        "notes": "Person mention remains non-authoritative because no reviewed identity ID is attached here.",
    },
    {
        "record_id": "entity-linking-02",
        "entity_type": "organisation",
        "example_class": "positive",
        "mention_text": "New Zealand Labour",
        "source_document_type": "Hansard - vote",
        "parliament_number": 47,
        "source_stable_id": "47HansS_20240625_067140000",
        "source_excerpt": "Noes 48 New Zealand Labour 34; Green Party of Aotearoa New Zealand 14.",
        "selector": {
            "selector_type": "exact",
            "exact": "New Zealand Labour",
            "source_stable_id": "47HansS_20240625_067140000",
        },
        "candidate_links": [
            {
                "candidate_id": "party-vote-new-zealand-labour",
                "candidate_label": "New Zealand Labour",
                "candidate_uri": None,
                "authority_source_id": "nz-parliament-parties-current",
                "authority_source_url": AUTHORITY_SOURCE_URLS["nz-parliament-parties-current"],
                "score": 0.97,
                "match_method": "exact-party-label",
                "linking_status": "linked",
            }
        ],
        "linking_status": "linked",
        "provenance": {
            "method": "exact-label-rule",
            "rule_bundle": "entity-linking-exploratory-rules-v0.1",
            "authority_sources": ["nz-parliament-parties-current"],
            "human_validation": False,
        },
        "validation_status": "exploratory-only",
        "review_status": "reviewed",
        "release_status": "sample-not-release",
        "notes": "Party label is the cleanest exploratory candidate in this bundle.",
    },
    {
        "record_id": "entity-linking-03",
        "entity_type": "place",
        "example_class": "unresolved",
        "mention_text": "Wigram",
        "source_document_type": "Hansard - speech",
        "parliament_number": 47,
        "source_stable_id": "47HansS_20240625_067140000",
        "source_excerpt": "Hon Dr MEGAN WOODS (Labour-Wigram): Thank you Mr Speaker.",
        "selector": {
            "selector_type": "exact",
            "exact": "Wigram",
            "source_stable_id": "47HansS_20240625_067140000",
        },
        "candidate_links": [],
        "linking_status": "unresolved",
        "provenance": {
            "method": "lexical-location-rule",
            "rule_bundle": "entity-linking-exploratory-rules-v0.1",
            "authority_sources": [],
            "human_validation": False,
        },
        "validation_status": "exploratory-only",
        "review_status": "reviewed",
        "release_status": "sample-not-release",
        "notes": "Electorate labels are not treated as place authority links in this bundle.",
    },
    {
        "record_id": "entity-linking-04",
        "entity_type": "legislation",
        "example_class": "positive",
        "mention_text": "Land Transport (Clean Vehicle Standard) Amendment Bill",
        "source_document_type": "Hansard - debate",
        "parliament_number": 47,
        "source_stable_id": "47HansS_20240625_067140000",
        "source_excerpt": "Land Transport (Clean Vehicle Standard) Amendment Bill - second reading",
        "selector": {
            "selector_type": "exact",
            "exact": "Land Transport (Clean Vehicle Standard) Amendment Bill",
            "source_stable_id": "47HansS_20240625_067140000",
        },
        "candidate_links": [
            {
                "candidate_id": "bill-land-transport-clean-vehicle-standard-amendment",
                "candidate_label": "Land Transport (Clean Vehicle Standard) Amendment Bill",
                "candidate_uri": None,
                "authority_source_id": "nz-parliament-bills-current",
                "authority_source_url": AUTHORITY_SOURCE_URLS["nz-parliament-bills-current"],
                "score": 0.95,
                "match_method": "exact-bill-title",
                "linking_status": "linked",
            }
        ],
        "linking_status": "linked",
        "provenance": {
            "method": "exact-title-rule",
            "rule_bundle": "entity-linking-exploratory-rules-v0.1",
            "authority_sources": ["nz-parliament-bills-current"],
            "human_validation": False,
        },
        "validation_status": "exploratory-only",
        "review_status": "reviewed",
        "release_status": "sample-not-release",
        "notes": "Bill titles are the best matched legislation surface in the sample set.",
    },
    {
        "record_id": "entity-linking-05",
        "entity_type": "ministry",
        "example_class": "unresolved",
        "mention_text": "Ministry of Transport",
        "source_document_type": "Hansard - speech",
        "parliament_number": 47,
        "source_stable_id": "47HansS_20240625_067140000",
        "source_excerpt": "the Ministry of Transport the Minister's officials had to give an exemption",
        "selector": {
            "selector_type": "exact",
            "exact": "Ministry of Transport",
            "source_stable_id": "47HansS_20240625_067140000",
        },
        "candidate_links": [],
        "linking_status": "unresolved",
        "provenance": {
            "method": "department-title-rule",
            "rule_bundle": "entity-linking-exploratory-rules-v0.1",
            "authority_sources": [],
            "human_validation": False,
        },
        "validation_status": "exploratory-only",
        "review_status": "reviewed",
        "release_status": "sample-not-release",
        "notes": "Ministry labels are deferred until a dated administrative authority source is added.",
    },
    {
        "record_id": "entity-linking-06",
        "entity_type": "portfolio",
        "example_class": "negative",
        "mention_text": "Minister of Consumer Affairs",
        "source_document_type": "Hansard - debate",
        "parliament_number": 47,
        "source_stable_id": "47HansD_20030408",
        "source_excerpt": "Minister of Consumer Affairs: I move",
        "selector": {
            "selector_type": "exact",
            "exact": "Minister of Consumer Affairs",
            "source_stable_id": "47HansD_20030408",
        },
        "candidate_links": [],
        "linking_status": "negative",
        "provenance": {
            "method": "office-title-exclusion-rule",
            "rule_bundle": "entity-linking-exploratory-rules-v0.1",
            "authority_sources": [],
            "human_validation": False,
        },
        "validation_status": "exploratory-only",
        "review_status": "reviewed",
        "release_status": "sample-not-release",
        "notes": "Office titles are explicitly excluded from authoritative entity resolution.",
    },
    {
        "record_id": "entity-linking-07",
        "entity_type": "committee",
        "example_class": "excluded",
        "mention_text": "committee stage",
        "source_document_type": "Hansard - speech",
        "parliament_number": 47,
        "source_stable_id": "47HansS_20240625_067140000",
        "source_excerpt": "This bill is set down for committee stage immediately.",
        "selector": {
            "selector_type": "exact",
            "exact": "committee stage",
            "source_stable_id": "47HansS_20240625_067140000",
        },
        "candidate_links": [],
        "linking_status": "excluded",
        "provenance": {
            "method": "procedural-phrase-exclusion-rule",
            "rule_bundle": "entity-linking-exploratory-rules-v0.1",
            "authority_sources": ["nz-parliament-order-paper", "nz-parliament-hansard-current"],
            "human_validation": False,
        },
        "validation_status": "exploratory-only",
        "review_status": "reviewed",
        "release_status": "sample-not-release",
        "notes": "Generic procedural phrases are excluded from entity-linking publication claims.",
    },
]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "record_id",
        "example_class",
        "entity_type",
        "mention_text",
        "source_document_type",
        "parliament_number",
        "source_stable_id",
        "source_excerpt",
        "selector",
        "candidate_links",
        "linking_status",
        "provenance",
        "validation_status",
        "review_status",
        "release_status",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            csv_row = dict(row)
            csv_row["selector"] = json.dumps(row["selector"], sort_keys=True)
            csv_row["candidate_links"] = json.dumps(row["candidate_links"], sort_keys=True)
            csv_row["provenance"] = json.dumps(row["provenance"], sort_keys=True)
            writer.writerow(csv_row)


def build_manifest(generated_at: str) -> dict[str, Any]:
    rows = ENTITY_LINKING_ROWS
    return {
        "manifest_version": 1,
        "track_id": "entity_linking_exploratory_outputs_20260610",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "release_status": "sample-not-release",
        "sample_package": "samples/entity-linking-exploratory",
        "outputs": {
            "jsonl": JSONL_PATH.relative_to(ROOT).as_posix(),
            "review_csv": REVIEW_PATH.relative_to(ROOT).as_posix(),
        },
        "source_inputs": [
            "samples/researcher-client-helpers/hansard-mini.csv",
            "samples/member-identity/member_identity_review.csv",
            "samples/party-attribution/party_attribution_review.csv",
            "samples/parlamint-nz/ParlaMint-NZ.sample.xml",
            "samples/popolo-opencivicdata/speeches.jsonl",
            "samples/rdf-linked-data/linked-data.ttl",
            "manifests/authority_sources.json",
            "manifests/schema_discovery.json",
        ],
        "supported_entity_types": [
            "person",
            "organisation",
            "place",
            "legislation",
            "ministry",
            "portfolio",
            "committee",
        ],
        "validation_counts": {
            "record_count": len(rows),
            "review_row_count": len(rows),
            "linked": sum(1 for row in rows if row["linking_status"] == "linked"),
            "ambiguous": sum(1 for row in rows if row["linking_status"] == "ambiguous"),
            "unresolved": sum(1 for row in rows if row["linking_status"] == "unresolved"),
            "negative": sum(1 for row in rows if row["linking_status"] == "negative"),
            "excluded": sum(1 for row in rows if row["linking_status"] == "excluded"),
        },
        "authority_sources": [
            "nz-parliament-members-current",
            "nz-parliament-parties-current",
            "nz-parliament-bills-current",
            "nz-parliament-order-paper",
            "nz-parliament-hansard-current",
            "nz-parliament-daily-progress",
            "nz-parliament-parliamentary-rules",
        ],
        "validation_results": {
            "outputs_written": True,
            "review_sample_written": True,
            "non_authoritative": True,
            "false_positive_analysis_recorded": True,
            "human_validation_required": True,
        },
    }


def build_entity_linking_exploratory_outputs(
    *, generated_at: str, write: bool = True
) -> dict[str, Any]:
    manifest = build_manifest(generated_at)
    if write:
        SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
        _write_jsonl(JSONL_PATH, ENTITY_LINKING_ROWS)
        _write_csv(REVIEW_PATH, ENTITY_LINKING_ROWS)
    return manifest
