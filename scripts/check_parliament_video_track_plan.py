"""Validate the Parliament video Conductor track plan discipline."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK_ROOT = ROOT / "conductor" / "tracks"
ARCHIVE_ROOT = ROOT / "conductor" / "archive"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
QUALITY_WORKFLOW = ROOT / ".github" / "workflows" / "quality.yml"
PIXI_TOML = ROOT / "pixi.toml"

TRACK_IDS = (
    "parliament_video_source_inventory_20260705",
    "parliament_video_seed_fetchers_20260705",
    "parliament_video_full_metadata_archive_20260705",
    "parliament_video_reconciliation_20260705",
    "parliament_video_media_acquisition_decision_20260705",
    "parliament_video_ongoing_archive_20260705",
)

SPEC_REQUIREMENTS = (
    "metadata-first/no-download",
    "official Parliament Video",
    "NZ Parliament YouTube",
    "Parliament On Demand",
    "Vimeo",
    "TVNZ Archive",
    "Ngā Taonga",
    "RNZ",
    "Parliament Today",
    "Archives New Zealand",
    "Internet Archive",
    "web archives",
)

PLAN_REQUIREMENTS = (
    "commit after each task",
    "git notes",
    "push to the remote after each phase",
    "GitHub Actions",
    "address any failing checks",
    "phase checkpoint",
    "no media download",
)

WORKFLOW_REQUIREMENTS = ("parliament-video-track-plan",)
PIXI_REQUIREMENTS = (
    "check_parliament_video_track_plan.py",
    "parliament-video-track-plan",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _missing_fragments(text: str, fragments: tuple[str, ...]) -> list[str]:
    folded = text.casefold()
    return [fragment for fragment in fragments if fragment.casefold() not in folded]


def _validate_track(track_id: str) -> list[str]:
    failures: list[str] = []
    active_dir = TRACK_ROOT / track_id
    archive_dir = ARCHIVE_ROOT / track_id
    track_dir = active_dir if active_dir.exists() else archive_dir
    for filename in ("spec.md", "plan.md", "metadata.json", "index.md"):
        path = track_dir / filename
        if not path.exists():
            failures.append(f"{track_id}/{filename} must exist.")
    if failures:
        return failures

    spec = _read(track_dir / "spec.md")
    plan = _read(track_dir / "plan.md")
    metadata = _read(track_dir / "metadata.json")
    index = _read(track_dir / "index.md")

    for fragment in _missing_fragments(spec, SPEC_REQUIREMENTS):
        failures.append(f"{track_id}/spec.md is missing required source/policy text: {fragment}")
    for fragment in _missing_fragments(plan, PLAN_REQUIREMENTS):
        failures.append(f"{track_id}/plan.md is missing required execution text: {fragment}")
    if '"track_id"' not in metadata or track_id not in metadata:
        failures.append(f"{track_id}/metadata.json must declare the track_id.")
    if "github_actions" not in metadata:
        failures.append(f"{track_id}/metadata.json must declare github_actions metadata.")
    for filename in ("spec.md", "plan.md", "metadata.json"):
        if filename not in index:
            failures.append(f"{track_id}/index.md must link {filename}.")
    return failures


def _failures() -> list[str]:
    failures: list[str] = []
    registry = _read(TRACKS_REGISTRY) if TRACKS_REGISTRY.exists() else ""
    for track_id in TRACK_IDS:
        if track_id not in registry:
            failures.append(f"conductor/tracks.md must register {track_id}.")
        failures.extend(_validate_track(track_id))

    if not QUALITY_WORKFLOW.exists():
        failures.append(".github/workflows/quality.yml must exist.")
    else:
        workflow_text = _read(QUALITY_WORKFLOW)
        for fragment in WORKFLOW_REQUIREMENTS:
            if fragment not in workflow_text:
                failures.append(f"quality.yml must include {fragment}.")

    if not PIXI_TOML.exists():
        failures.append("pixi.toml must exist.")
    else:
        pixi_text = _read(PIXI_TOML)
        for fragment in PIXI_REQUIREMENTS:
            if fragment not in pixi_text:
                failures.append(f"pixi.toml must include {fragment}.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-VIDEO-TRACK-PLAN: {failure}")
        return 1
    print("Parliament video Conductor track plans are CI-visible and execution-ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
