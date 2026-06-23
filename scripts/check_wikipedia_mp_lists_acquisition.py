"""Validate the Wikipedia MP lists acquisition track evidence."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "wikipedia_mp_lists_acquisition_20260612"
TRACK_DIR = ROOT / "conductor" / "tracks" / TRACK_ID
OUTPUT_PATH = ROOT / "derived" / "wikipedia_mp_lists.json"
EXPECTED_COUNTS = {
    "47": 122,
    "48": 132,
    "49": 132,
    "50": 132,
    "51": 128,
    "52": 125,
    "53": 124,
}
EXPECTED_PARLIAMENTS = set(EXPECTED_COUNTS)
EXPECTED_ARTICLES = {
    "47": "47th_New_Zealand_Parliament",
    "48": "48th_New_Zealand_Parliament",
    "49": "49th_New_Zealand_Parliament",
    "50": "50th_New_Zealand_Parliament",
    "51": "51st_New_Zealand_Parliament",
    "52": "52nd_New_Zealand_Parliament",
    "53": "53rd_New_Zealand_Parliament",
}
EXPECTED_TOTAL = sum(EXPECTED_COUNTS.values())
ALLOWED_PARTIES = {
    "ACT",
    "Green",
    "Independent",
    "Labour",
    "Mana",
    "Maori Party",
    "National",
    "NZ First",
    "Progressive",
    "United Future",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FETCHED_AT_RE = re.compile(r"^20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$")


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _failures() -> list[str]:
    failures: list[str] = []
    if not OUTPUT_PATH.exists():
        failures.append("derived/wikipedia_mp_lists.json is missing.")
        return failures

    data = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    members_by_parliament = data.get("members_by_parliament", {})
    if set(members_by_parliament) != EXPECTED_PARLIAMENTS:
        failures.append(
            "members_by_parliament must cover Parliaments 47-53 exactly; "
            f"found {sorted(members_by_parliament)}."
        )

    total = data.get("total_mps")
    counted_total = sum(len(rows) for rows in members_by_parliament.values())
    if total != counted_total:
        failures.append(f"total_mps {total!r} does not match counted total {counted_total}.")
    if counted_total != EXPECTED_TOTAL:
        failures.append(f"Expected exactly {EXPECTED_TOTAL} MP references; found {counted_total}.")

    for parliament, expected_count in EXPECTED_COUNTS.items():
        count = len(members_by_parliament.get(parliament, []))
        if count != expected_count:
            failures.append(
                f"Parliament {parliament} has {count} rows; expected {expected_count}."
            )

    source_articles = data.get("source_articles", {})
    if set(source_articles) != EXPECTED_PARLIAMENTS:
        failures.append(
            "source_articles must cover Parliaments 47-53 exactly; "
            f"found {sorted(source_articles)}."
        )
    for parliament, source in source_articles.items():
        article = EXPECTED_ARTICLES[parliament]
        expected_url = f"https://en.wikipedia.org/api/rest_v1/page/html/{article}"
        if source.get("article") != article:
            failures.append(
                f"Parliament {parliament} source article must be {article!r}; "
                f"found {source.get('article')!r}."
            )
        if source.get("url") != expected_url:
            failures.append(
                f"Parliament {parliament} source URL must be {expected_url!r}; "
                f"found {source.get('url')!r}."
            )
        if source.get("status") != "ok":
            failures.append(f"Parliament {parliament} source status must be ok.")
        if not FETCHED_AT_RE.fullmatch(source.get("fetched_at", "")):
            failures.append(f"Parliament {parliament} source fetched_at must be UTC ISO seconds.")
        if not SHA256_RE.fullmatch(source.get("html_sha256", "")):
            failures.append(f"Parliament {parliament} source html_sha256 must be a SHA-256 hex digest.")

    if not FETCHED_AT_RE.fullmatch(data.get("fetched_at", "")):
        failures.append("Top-level fetched_at must be UTC ISO seconds.")

    parties = Counter()
    for parliament, rows in members_by_parliament.items():
        for index, row in enumerate(rows):
            for field in ("name", "party", "electorate", "wiki_slug"):
                if not row.get(field):
                    failures.append(f"Parliament {parliament} row {index} has empty {field}.")
            party = row.get("party", "")
            parties[party] += 1
            if party not in ALLOWED_PARTIES:
                failures.append(
                    f"Parliament {parliament} row {index} has unsupported party label {party!r}."
                )
    if not {"Labour", "National", "Green", "ACT"}.issubset(parties):
        failures.append(
            f"Expected major party labels missing from aggregate parties: {sorted(parties)}."
        )

    metadata = json.loads((TRACK_DIR / "metadata.json").read_text(encoding="utf-8"))
    if metadata.get("status") not in {"complete", "archived"}:
        failures.append("Wikipedia MP lists metadata status must be complete or archived.")

    evidence = (TRACK_DIR / "evidence.md").read_text(encoding="utf-8")
    for snippet in (
        "895 MP records",
        "source_articles",
        "html_sha256",
        "scripts/check_wikipedia_mp_lists_acquisition.py",
        "47th | 47th_New_Zealand_Parliament | 122",
        "48th | 48th_New_Zealand_Parliament | 132",
        "49th | 49th_New_Zealand_Parliament | 132",
        "50th | 50th_New_Zealand_Parliament | 132",
        "51st | 51st_New_Zealand_Parliament | 128",
        "52nd | 52nd_New_Zealand_Parliament | 125",
        "53rd | 53rd_New_Zealand_Parliament | 124",
    ):
        if snippet not in evidence:
            failures.append(f"Evidence is missing: {snippet}")

    tracks = _read("conductor/tracks.md")
    if "### [x] Track: Wikipedia MP Lists Acquisition" not in tracks or TRACK_ID not in tracks:
        failures.append("conductor/tracks.md must list the Wikipedia MP lists track.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"WIKIPEDIA-MP-LISTS: {failure}")
        return 1
    print("Wikipedia MP lists acquisition evidence is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
