"""Validate the NZ Parliament video source inventory."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_source_inventory.json"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_source_inventory.schema.json"
DOC_PATH = ROOT / "docs" / "parliament-video-source-inventory.md"
TRACK_PLAN_PATHS = (
    ROOT / "conductor/tracks/parliament_video_source_inventory_20260705/plan.md",
    ROOT / "conductor/archive/parliament_video_source_inventory_20260705/plan.md",
)

REQUIRED_SOURCE_FAMILIES = {
    "house_video",
    "select_committee_video",
    "parliament_website_embeds",
    "social_video_platform",
    "broadcast_archive",
    "audio_reporting",
    "web_archive",
    "adjacent_repo_evidence",
}
REQUIRED_PLATFORM_CLASSES = {
    "official_parliament_video",
    "official_parliament_website",
    "youtube",
    "vimeo",
    "parliament_on_demand",
    "broadcast_catalogue",
    "audio_reporting",
    "web_archive",
    "repository",
    "search_or_sitemap",
}
REQUIRED_FALLBACK_ROLES = {
    "not_fallback",
    "historical_broadcast_validation",
    "catalogue_validation",
    "audio_or_reporting_validation",
    "link_rot_validation",
    "boundary_evidence",
}
REQUIRED_OFFICIAL_SOURCE_IDS = {
    "official-parliament-video",
    "official-parliament-live-and-recorded",
    "official-youtube-nz-parliament",
    "parliament-on-demand-house-archive",
    "select-committee-on-demand-archive",
    "select-committee-live-streams-current",
    "select-committee-vimeo-pages",
    "parliament-website-embedded-video-pages",
    "parliament-site-search-and-sitemaps",
}
REQUIRED_FALLBACK_SOURCE_IDS = {
    "tvnz-archive-looking-back",
    "nga-taonga-av-collection",
    "rnz-parliament",
    "parliament-today-am-network",
    "archives-new-zealand-av-catalogue",
    "internet-archive-webcaptures",
    "memento-cdx-web-archives",
}
REQUIRED_ADJACENT_SOURCE_IDS = {
    "adjacent-sm-govt-nz",
    "adjacent-hathi-nz",
    "adjacent-corpus-law-nz",
}
REQUIRED_POLICY_FLAGS = {
    "metadata_first",
    "no_media_download",
    "no_video_file_download",
    "no_audio_file_download",
    "no_public_media_release",
    "no_completeness_claim",
    "fallbacks_are_validation_only",
    "rights_review_required_before_media_acquisition",
}


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


def _role_counts(sources: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "official": sum(1 for source in sources if source.get("source_role") == "official"),
        "fallback": sum(1 for source in sources if source.get("source_role") == "fallback"),
        "supporting": sum(1 for source in sources if source.get("source_role") == "supporting"),
    }


def _validate_manifest(manifest: dict[str, Any]) -> list[str]:
    failures = _schema_failures(manifest)
    taxonomy = manifest.get("taxonomy", {})
    sources = manifest.get("sources", [])
    source_ids = [source.get("source_id") for source in sources]
    sources_by_id = {source["source_id"]: source for source in sources if "source_id" in source}

    if set(taxonomy.get("source_families", [])) != REQUIRED_SOURCE_FAMILIES:
        failures.append("taxonomy.source_families must exactly match the required source families.")
    if set(taxonomy.get("platform_classes", [])) != REQUIRED_PLATFORM_CLASSES:
        failures.append(
            "taxonomy.platform_classes must exactly match the required platform classes."
        )
    if set(taxonomy.get("fallback_roles", [])) != REQUIRED_FALLBACK_ROLES:
        failures.append("taxonomy.fallback_roles must exactly match the required fallback roles.")

    duplicate_ids = sorted(
        {source_id for source_id in source_ids if source_ids.count(source_id) > 1}
    )
    for source_id in duplicate_ids:
        failures.append(f"Duplicate source id: {source_id}")

    missing_official = REQUIRED_OFFICIAL_SOURCE_IDS - set(sources_by_id)
    if missing_official:
        failures.append("missing official source ids: " + ", ".join(sorted(missing_official)))
    missing_fallback = REQUIRED_FALLBACK_SOURCE_IDS - set(sources_by_id)
    if missing_fallback:
        failures.append("missing fallback source ids: " + ", ".join(sorted(missing_fallback)))
    missing_adjacent = REQUIRED_ADJACENT_SOURCE_IDS - set(sources_by_id)
    if missing_adjacent:
        failures.append("missing adjacent repo source ids: " + ", ".join(sorted(missing_adjacent)))

    for source in sources:
        source_id = source.get("source_id", "<missing>")
        role = source.get("source_role")
        media_types = set(source.get("media_types", []))
        if role == "official":
            if source.get("publisher") != "New Zealand Parliament":
                failures.append(
                    f"{source_id} official source must use New Zealand Parliament publisher."
                )
            if (
                source.get("platform_class") in {"youtube", "vimeo"}
                and source.get("rights_status") != "platform_terms_review_required"
            ):
                failures.append(f"{source_id} platform source must require platform terms review.")
            if source.get("fallback_role") != "not_fallback":
                failures.append(f"{source_id} official source must use fallback_role=not_fallback.")
            if source.get("acquisition_boundary") != "metadata_only_no_media_download":
                failures.append(f"{source_id} official source must be metadata-only.")
            if "metadata" not in media_types:
                failures.append(f"{source_id} official source must expose metadata.")
        elif role == "fallback":
            if source.get("acquisition_boundary") != "validation_only_no_media_download":
                failures.append(f"{source_id} fallback source must be validation-only.")
            if media_types != {"metadata"}:
                failures.append(f"{source_id} fallback source must not list media downloads.")
            if source.get("archive_status") != "fallback_evidence_only":
                failures.append(f"{source_id} fallback source must be fallback_evidence_only.")
            if source.get("fallback_role") in {"", None, "not_fallback"}:
                failures.append(f"{source_id} fallback source must declare a validation role.")
        elif role == "supporting":
            if source.get("source_family") != "adjacent_repo_evidence":
                failures.append(f"{source_id} supporting source must be adjacent_repo_evidence.")
            if source.get("acquisition_boundary") != "evidence_only_no_media_download":
                failures.append(f"{source_id} supporting source must be evidence-only.")
            if media_types != {"metadata"}:
                failures.append(f"{source_id} supporting source must not list media downloads.")
            if source.get("rights_status") != "not_media_source":
                failures.append(f"{source_id} supporting source must be not_media_source.")
        else:
            failures.append(f"{source_id} has unsupported source_role: {role}")

    summary = manifest.get("source_summary", {})
    counts = _role_counts(sources)
    if summary.get("source_count") != len(sources):
        failures.append("source_summary.source_count must match sources length.")
    if summary.get("official_source_count") != counts["official"]:
        failures.append("source_summary.official_source_count must match official sources.")
    if summary.get("fallback_source_count") != counts["fallback"]:
        failures.append("source_summary.fallback_source_count must match fallback sources.")
    if summary.get("supporting_source_count") != counts["supporting"]:
        failures.append("source_summary.supporting_source_count must match supporting sources.")
    if set(summary.get("official_source_ids", [])) != REQUIRED_OFFICIAL_SOURCE_IDS:
        failures.append("source_summary.official_source_ids must match the required official ids.")
    if set(summary.get("fallback_source_ids", [])) != REQUIRED_FALLBACK_SOURCE_IDS:
        failures.append("source_summary.fallback_source_ids must match the required fallback ids.")

    fallback_ids_by_role = summary.get("fallback_ids_by_role", {})
    for role in REQUIRED_FALLBACK_ROLES - {"not_fallback"}:
        ids = set(fallback_ids_by_role.get(role, []))
        if not ids:
            failures.append(f"source_summary.fallback_ids_by_role.{role} must not be empty.")
        for source_id in ids:
            if source_id not in sources_by_id:
                failures.append(f"fallback role {role} references missing source id: {source_id}")
            elif sources_by_id[source_id]["fallback_role"] != role:
                failures.append(
                    f"fallback role {role} references source with different role: {source_id}"
                )

    family_coverage = manifest.get("family_coverage", {})
    if set(family_coverage) != REQUIRED_SOURCE_FAMILIES:
        failures.append("family_coverage must cover every source family.")
    for family, coverage in family_coverage.items():
        if coverage.get("completion_claim") != "inventory-only-no-completeness-claim":
            failures.append(f"{family} has unsupported completion claim.")
        for source_id in coverage.get("primary_source_ids", []) + coverage.get(
            "fallback_source_ids", []
        ):
            if source_id not in sources_by_id:
                failures.append(f"{family} references missing source id: {source_id}")
            elif sources_by_id[source_id]["source_family"] != family:
                failures.append(f"{family} references source with different family: {source_id}")

    policy = manifest.get("policy", {})
    for flag in sorted(REQUIRED_POLICY_FLAGS):
        if policy.get(flag) is not True:
            failures.append(f"policy.{flag} must be true.")

    return failures


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    track_plan_path = next((path for path in TRACK_PLAN_PATHS if path.exists()), None)
    if track_plan_path is None:
        failures.append("Parliament video source inventory track plan must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    failures.extend(_validate_manifest(manifest))

    doc = _read(DOC_PATH)
    for required in (
        "metadata-first/no-download source inventory",
        "No media download",
        "No completeness claim",
        "Fallback resources are validation-only",
        "parliament_video_seed_fetchers_20260705",
        "sm-govt-nz",
        "hathi-nz",
        "corpus-law-nz",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    plan = _read(track_plan_path)
    if "No media download is allowed" not in plan:
        failures.append("track plan must preserve the no-media-download rule.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-VIDEO-SOURCE-INVENTORY: {failure}")
        return 1
    print("Parliament video source inventory is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
