"""Build the static documentation portal from repository docs and manifests."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/static_documentation_portal_manifest.json"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
PUBLIC_RELEASE_PATH = ROOT / "manifests/public_dataset_release_manifest.json"
TRACKS_PATH = ROOT / "conductor/tracks.md"
PORTAL_DIR = ROOT / "docs/static-documentation-portal"
HTML_PATH = PORTAL_DIR / "index.html"
SOURCE_DOC_PATH = ROOT / "docs/static-documentation-portal.md"

TRACK_HEADING_RE = re.compile(r"^### \[(?P<status>.)\] Track: (?P<title>.+)$")
TRACK_ID_RE = re.compile(r"^Track ID: `(?P<track_id>[^`]+)`$")
LINK_RE = re.compile(r"^Link: \[(?P<label>.+)\]\((?P<link>.+)\)$")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parse_tracks(tracks_text: str) -> list[dict[str, str]]:
    tracks: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in tracks_text.splitlines():
        heading = TRACK_HEADING_RE.match(line)
        if heading:
            status = heading.group("status")
            current = {"status": status, "title": heading.group("title")}
            tracks.append(current)
            continue
        if current is None:
            continue
        track_id = TRACK_ID_RE.match(line)
        if track_id:
            current["track_id"] = track_id.group("track_id")
            continue
        if line.startswith("Goal: "):
            current["goal"] = line[len("Goal: ") :]
            continue
        link = LINK_RE.match(line)
        if link:
            current["link"] = link.group("link")
    return [
        {
            "status": item.get("status", "[ ]"),
            "title": item.get("title", ""),
            "track_id": item.get("track_id", ""),
            "goal": item.get("goal", ""),
            "link": item.get("link", ""),
        }
        for item in tracks
    ]


def _status_label(status: str) -> str:
    return {"x": "complete", "!": "blocked", "~": "in progress"}.get(status, "pending")


def _render_list(items: list[dict[str, str]]) -> str:
    rows = []
    for item in items:
        path = item["path"]
        relative = path.replace("docs/", "", 1)
        label = html.escape(item["label"])
        rows.append(
            f"<tr><td>{label}</td><td><a href='../{html.escape(relative)}'>{html.escape(relative)}</a></td></tr>"
        )
    return "\n".join(rows)


def _render_tracks(tracks: list[dict[str, str]]) -> str:
    rows = []
    for track in tracks:
        rows.append(
            "<tr>"
            f"<td>{html.escape(_status_label(track['status']))}</td>"
            f"<td>{html.escape(track['title'])}</td>"
            f"<td><code>{html.escape(track['track_id'])}</code></td>"
            f"<td>{html.escape(track['goal'])}</td>"
            f"<td><a href='../../{html.escape(track['link'].lstrip('./'))}'>{html.escape(track['link'])}</a></td>"
            "</tr>"
        )
    return "\n".join(rows)


def _render_release_levels(release_levels: list[dict[str, Any]]) -> str:
    rows = []
    for level in release_levels:
        rows.append(
            "<tr>"
            f"<td>{level['level']}</td>"
            f"<td><code>{html.escape(level['id'])}</code></td>"
            f"<td>{html.escape(_level_status(level['level']))}</td>"
            f"<td>{html.escape(level['description'])}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _render_artifact_map(artifact_map: list[dict[str, Any]]) -> str:
    rows = []
    for item in artifact_map:
        rows.append(
            "<tr>"
            f"<td>{html.escape(item['artifact'])}</td>"
            f"<td><code>{html.escape(item['path'])}</code></td>"
            f"<td>{html.escape(item['release_level'])}</td>"
            f"<td>{html.escape(item['status'])}</td>"
            f"<td>{html.escape(item['next_gate'])}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _level_status(level: int) -> str:
    return {
        1: "published",
        2: "validated-manifest",
        3: "validated-manifest",
        4: "planned",
        5: "planned",
    }.get(level, "planned")


def _build_manifest(
    *,
    generated_at: str,
    tracks: list[dict[str, str]],
    release_ladder: dict[str, Any],
    public_release: dict[str, Any],
) -> dict[str, Any]:
    status_counts = Counter(_status_label(track["status"]) for track in tracks)
    citation_guidance = [
        {"label": "Release ladder", "path": "docs/release-ladder.md"},
        {"label": "Publication status", "path": "docs/publication-status.md"},
        {"label": "Public release checklist", "path": "docs/public-release-checklist.md"},
        {"label": "Release evidence ledger", "path": "docs/release-evidence-ledger.md"},
        {"label": "Licensing and provenance", "path": "docs/licensing-and-provenance.md"},
        {"label": "Canonical ID and URI policy", "path": "docs/canonical-id-uri-policy.md"},
    ]
    data_dictionary = [
        {"label": "Shared NZ corpus core schema", "path": "docs/shared-nz-corpus-core-schema.md"},
        {"label": "Neutral component model", "path": "docs/neutral-component-model.md"},
        {"label": "Endpoint contracts", "path": "docs/endpoint-contracts.md"},
        {"label": "Derived fields validation", "path": "docs/derived-fields-validation.md"},
        {"label": "Member identity resolution", "path": "docs/member-identity-resolution.md"},
        {"label": "Party attribution provenance", "path": "docs/party-attribution-provenance.md"},
        {
            "label": "Speech-turn segmentation contract",
            "path": "docs/speech-turn-segmentation-contract.md",
        },
    ]
    return {
        "manifest_version": 1,
        "track_id": "static_documentation_portal_20260610",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "site_root": HTML_PATH.relative_to(ROOT).as_posix(),
        "build_outputs": {
            "html": HTML_PATH.relative_to(ROOT).as_posix(),
            "source_doc": SOURCE_DOC_PATH.relative_to(ROOT).as_posix(),
        },
        "sources": {
            "release_ladder": RELEASE_LADDER_PATH.relative_to(ROOT).as_posix(),
            "public_release_manifest": PUBLIC_RELEASE_PATH.relative_to(ROOT).as_posix(),
            "track_registry": TRACKS_PATH.relative_to(ROOT).as_posix(),
            "publication_status": "docs/publication-status.md",
            "public_release_checklist": "docs/public-release-checklist.md",
        },
        "current_public_release": {
            "version": public_release["publication"]["github_release"].split("/tag/v")[-1],
            "release_level": release_ladder["current_public_release"]["release_level"],
            "publication_status": public_release["publication_status"],
            "github_release": public_release["publication"]["github_release"],
            "huggingface_dataset": public_release["publication"]["huggingface_dataset"],
            "zenodo_record": public_release["publication"]["zenodo_record"],
        },
        "release_ladder_snapshot": {
            "current_public_release": release_ladder["current_public_release"],
            "release_levels": [
                {"level": item["level"], "id": item["id"], "status": _level_status(item["level"])}
                for item in release_ladder["release_levels"]
            ],
            "artifact_map_count": len(release_ladder["artifact_map"]),
        },
        "track_snapshot": {
            "summary_counts": {
                "complete": status_counts.get("complete", 0),
                "blocked": status_counts.get("blocked", 0),
                "pending": status_counts.get("pending", 0),
            },
            "tracks": tracks,
        },
        "reference_catalog": {
            "citation_guidance": citation_guidance,
            "data_dictionary": data_dictionary,
        },
        "validation_results": {
            "portal_built": True,
            "current_public_release_version": "0.1.0",
            "track_rows": len(tracks),
            "public_release_urls_recorded": True,
        },
    }


def _render_html(manifest: dict[str, Any], release_ladder: dict[str, Any]) -> str:
    citation_rows = _render_list(manifest["reference_catalog"]["citation_guidance"])
    data_rows = _render_list(manifest["reference_catalog"]["data_dictionary"])
    track_rows = _render_tracks(manifest["track_snapshot"]["tracks"])
    level_rows = _render_release_levels(release_ladder["release_levels"])
    artifact_rows = _render_artifact_map(release_ladder["artifact_map"])
    release = manifest["current_public_release"]

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Static Documentation Portal</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f2;
      --panel: #ffffff;
      --ink: #1f2328;
      --muted: #5f6b7a;
      --line: #d7dde5;
      --accent: #2856a7;
      --good: #20744f;
      --warn: #8a5a00;
    }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
    }}
    main {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    h1, h2, h3 {{
      margin: 0 0 12px;
      line-height: 1.2;
    }}
    h1 {{
      font-size: 2rem;
    }}
    h2 {{
      margin-top: 32px;
      font-size: 1.15rem;
    }}
    p, li {{
      line-height: 1.5;
      color: var(--muted);
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      margin-top: 16px;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }}
    .stat {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #fcfcfb;
    }}
    .stat strong {{
      display: block;
      font-size: 1.4rem;
      color: var(--ink);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      font-size: 0.95rem;
    }}
    th, td {{
      border-top: 1px solid var(--line);
      padding: 10px 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.02em;
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      font-size: 0.9em;
    }}
    a {{
      color: var(--accent);
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .note {{
      color: var(--muted);
      font-size: 0.95rem;
    }}
    .grid-two {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }}
    @media (max-width: 900px) {{
      .stats, .grid-two {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <h1>Static Documentation Portal</h1>
    <p class="note">
      Generated from repository docs and manifests. This page is a static status surface, not a separate source of truth.
    </p>

    <section class="panel">
      <h2>Current Public Release</h2>
      <div class="stats">
        <div class="stat"><span>Version</span><strong>{html.escape(release["version"])}</strong></div>
        <div class="stat"><span>Level</span><strong>{html.escape(release["release_level"])}</strong></div>
        <div class="stat"><span>Status</span><strong>{html.escape(release["publication_status"])}</strong></div>
        <div class="stat"><span>Track rows</span><strong>{manifest["validation_results"]["track_rows"]}</strong></div>
      </div>
      <table>
        <thead><tr><th>Surface</th><th>URL</th></tr></thead>
        <tbody>
          <tr><td>GitHub release</td><td><a href="{html.escape(release["github_release"])}">{html.escape(release["github_release"])}</a></td></tr>
          <tr><td>Hugging Face dataset</td><td><a href="{html.escape(release["huggingface_dataset"])}">{html.escape(release["huggingface_dataset"])}</a></td></tr>
          <tr><td>Zenodo record</td><td><a href="{html.escape(release["zenodo_record"])}">{html.escape(release["zenodo_record"])}</a></td></tr>
        </tbody>
      </table>
    </section>

    <section class="panel">
      <h2>Release Ladder</h2>
      <p class="note">The ladder separates document-level release, authority-source evidence, neutral components, endpoints, and upstream contribution packages.</p>
      <table>
        <thead><tr><th>Level</th><th>ID</th><th>Status</th><th>Description</th></tr></thead>
        <tbody>
          {level_rows}
        </tbody>
      </table>
      <h3>Artifact Map</h3>
      <table>
        <thead><tr><th>Artifact</th><th>Path</th><th>Level</th><th>Status</th><th>Next gate</th></tr></thead>
        <tbody>
          {artifact_rows}
        </tbody>
      </table>
    </section>

    <div class="grid-two">
      <section class="panel">
        <h2>Track Status</h2>
        <div class="stats">
          <div class="stat"><span>Complete</span><strong>{manifest["track_snapshot"]["summary_counts"]["complete"]}</strong></div>
          <div class="stat"><span>Blocked</span><strong>{manifest["track_snapshot"]["summary_counts"]["blocked"]}</strong></div>
          <div class="stat"><span>Pending</span><strong>{manifest["track_snapshot"]["summary_counts"]["pending"]}</strong></div>
          <div class="stat"><span>Total</span><strong>{manifest["validation_results"]["track_rows"]}</strong></div>
        </div>
        <table>
          <thead><tr><th>Status</th><th>Track</th><th>Track ID</th><th>Goal</th><th>Link</th></tr></thead>
          <tbody>
            {track_rows}
          </tbody>
        </table>
      </section>

      <section class="panel">
        <h2>Citation Guidance</h2>
        <p class="note">Use these surfaces when citing release posture, provenance, or publication status.</p>
        <table>
          <thead><tr><th>Label</th><th>Path</th></tr></thead>
          <tbody>
            {citation_rows}
          </tbody>
        </table>

        <h2>Data Dictionaries</h2>
        <p class="note">These are the primary repo docs for data model, endpoint, and derived-field semantics.</p>
        <table>
          <thead><tr><th>Label</th><th>Path</th></tr></thead>
          <tbody>
            {data_rows}
          </tbody>
        </table>
      </section>
    </div>

    <section class="panel">
      <h2>Claim Boundary</h2>
      <p class="note">
        Public release surfaces are the GitHub release, Hugging Face dataset, and Zenodo record shown above.
        Sample-only endpoints, local review packages, and blocked tracks remain outside the public release claim.
      </p>
      <p class="note">
        Build source: {html.escape(SOURCE_DOC_PATH.relative_to(ROOT).as_posix())}, {html.escape(TRACKS_PATH.relative_to(ROOT).as_posix())},
        {html.escape(RELEASE_LADDER_PATH.relative_to(ROOT).as_posix())}, and {html.escape(PUBLIC_RELEASE_PATH.relative_to(ROOT).as_posix())}.
      </p>
    </section>
  </main>
</body>
</html>
"""


def build_static_documentation_portal(
    *, manifest_path: Path = MANIFEST_PATH, generated_at: str | None = None
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    release_ladder = _read_json(RELEASE_LADDER_PATH)
    public_release = _read_json(PUBLIC_RELEASE_PATH)
    tracks = _parse_tracks(_read_text(TRACKS_PATH))
    manifest = _build_manifest(
        generated_at=generated_at,
        tracks=tracks,
        release_ladder=release_ladder,
        public_release=public_release,
    )
    _write_json(manifest_path, manifest)
    PORTAL_DIR.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text(_render_html(manifest, release_ladder), encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the static documentation portal.")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_static_documentation_portal(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Wrote {HTML_PATH}")
    print(f"Tracks rendered: {manifest['validation_results']['track_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
