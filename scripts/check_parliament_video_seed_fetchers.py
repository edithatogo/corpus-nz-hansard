"""Validate Parliament video seed-fetcher outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_seed_fetchers.json"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_seed_fetchers.schema.json"
DOC_PATH = ROOT / "docs" / "parliament-video-seed-fetchers.md"
INVENTORY_PATH = ROOT / "manifests" / "parliament_video_source_inventory.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _schema_failures(manifest: dict[str, Any]) -> list[str]:
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures: list[str] = []
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")
    return failures


def _validate_manifest(manifest: dict[str, Any]) -> list[str]:
    failures = _schema_failures(manifest)
    inventory = _json(INVENTORY_PATH)
    inventory_by_id = {source["source_id"]: source for source in inventory["sources"]}
    records = manifest.get("targets", [])

    if manifest.get("summary", {}).get("target_count") != len(records):
        failures.append("summary.target_count must match targets length.")

    policy = manifest.get("policy", {})
    for key in (
        "metadata_first",
        "no_media_download",
        "no_video_file_download",
        "no_audio_file_download",
        "no_public_media_release",
        "no_completeness_claim",
        "fallbacks_are_validation_only",
        "rights_review_required_before_media_acquisition",
    ):
        if policy.get(key) is not True:
            failures.append(f"policy.{key} must be true.")

    source_ids = [record.get("source_id") for record in records]
    duplicate_ids = sorted(
        {source_id for source_id in source_ids if source_ids.count(source_id) > 1}
    )
    for source_id in duplicate_ids:
        failures.append(f"Duplicate source id: {source_id}")

    for record in records:
        source_id = record.get("source_id", "<missing>")
        inventory_source = inventory_by_id.get(source_id)
        if inventory_source is None:
            failures.append(f"{source_id} is not present in the video inventory manifest.")
            continue
        if record.get("source_role") != inventory_source.get("source_role"):
            failures.append(f"{source_id} source_role must match the inventory manifest.")
        if record.get("source_family") != inventory_source.get("source_family"):
            failures.append(f"{source_id} source_family must match the inventory manifest.")
        if record.get("rights_status") != inventory_source.get("rights_status"):
            failures.append(f"{source_id} rights_status must match the inventory manifest.")

        proof_status = record.get("proof_status")
        if proof_status == "fetched":
            if not record.get("index_sha256") or not record.get("sample_sha256"):
                failures.append(f"{source_id} fetched proof must carry both hashes.")
            if not record.get("sample_url"):
                failures.append(f"{source_id} fetched proof must record a sample_url.")
            if "index" not in record.get("output_paths", {}):
                failures.append(f"{source_id} fetched proof must record an index output path.")
        elif proof_status == "index-only":
            if not record.get("index_sha256"):
                failures.append(f"{source_id} index-only proof must carry an index hash.")
            if "index" not in record.get("output_paths", {}):
                failures.append(f"{source_id} index-only proof must record an index output path.")
        elif proof_status == "blocked":
            if not record.get("blocked_reason"):
                failures.append(f"{source_id} blocked proof must declare blocked_reason.")
        elif proof_status == "evidence-only":
            if record.get("request_urls"):
                failures.append(f"{source_id} evidence-only proof must not make network requests.")
        else:
            failures.append(f"{source_id} has unsupported proof_status: {proof_status}")

        if len(record.get("request_urls", [])) > 2:
            failures.append(f"{source_id} must keep request_urls bounded.")

    return failures


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH, INVENTORY_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures
    failures.extend(_validate_manifest(_json(MANIFEST_PATH)))
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-VIDEO-SEED-FETCHERS: {failure}")
        return 1
    print("Parliament video seed-fetcher manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
