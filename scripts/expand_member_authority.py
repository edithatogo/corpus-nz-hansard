"""Expand member identity authority source from corpus data."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

try:
    from scripts.build_member_identity_review import _normalize_token
    from scripts.canonical_ids import canonical_id, component_payload
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_member_identity_review import _normalize_token
    from scripts.canonical_ids import canonical_id, component_payload

ROOT = Path(__file__).resolve().parents[1]
PARQUET_PATH = ROOT / "generated/parquet/hansard.parquet"
AUTHORITY_PATH = ROOT / "derived/corpus_wide_member_identity_authority.json"
TRIANGULATED_PATH = ROOT / "derived/triangulated_member_authority.json"

IGNORED_TOKENS = {
    "",
    "Vacant",
    "Speaker",
    "Mr Speaker",
    "Madam Speaker",
    "Presiding Officer",
    "The Clerk",
    "Clerk",
    "Ang",
    "Richard Posser",
}

# Minimum token length: tokens shorter than this (after normalization) are skipped.
MIN_TOKEN_LENGTH = 3

# Common first names used to detect reversed-name tokens (e.g. "Foster-Bell Paul").
KNOWN_FIRST_NAMES = {
    "AARON",
    "ADAM",
    "ADRIAN",
    "ALAN",
    "ALASTAIR",
    "ALEX",
    "ALEXANDER",
    "ALLAN",
    "ANDREW",
    "ANGELA",
    "ANNE",
    "ANNETTE",
    "ANTHONY",
    "ARTHUR",
    "BARBARA",
    "BARRY",
    "BILL",
    "BRENT",
    "BRETT",
    "BRIAN",
    "BRUCE",
    "CARMEL",
    "CAROL",
    "CATHERINE",
    "CHARLES",
    "CHRIS",
    "CHRISTOPHER",
    "CLAYTON",
    "COLIN",
    "CRAIG",
    "DAME",
    "DANA",
    "DARREN",
    "DAVID",
    "DEBORAH",
    "DENISE",
    "DENNIS",
    "DIANNE",
    "DOMINIC",
    "DONALD",
    "DONNA",
    "DOUG",
    "DOUGLAS",
    "DUNCAN",
    "EDWARD",
    "ELIZABETH",
    "ERIC",
    "ERICA",
    "ERNEST",
    "FRANK",
    "FRASER",
    "FREDERICK",
    "GARRY",
    "GAVIN",
    "GEOFFREY",
    "GEORGE",
    "GERALD",
    "GERRY",
    "GORDON",
    "GRAEME",
    "GRANT",
    "GREG",
    "GREGORY",
    "HAMISH",
    "HELEN",
    "HENRY",
    "HILARY",
    "HUGH",
    "IAIN",
    "IAN",
    "JACK",
    "JACINDA",
    "JACQUI",
    "JAMES",
    "JAMIE",
    "JAN",
    "JANE",
    "JANET",
    "JEANETTE",
    "JENNY",
    "JEREMY",
    "JILL",
    "JIM",
    "JOANNE",
    "JOHN",
    "JONATHAN",
    "JOSEPH",
    "JUDITH",
    "JULIE",
    "JUSTIN",
    "KAREN",
    "KATHERINE",
    "KATHRYN",
    "KEITH",
    "KEN",
    "KENNETH",
    "KEVIN",
    "KIRSTY",
    "LAN",
    "LAURA",
    "LAURIE",
    "LAWRENCE",
    "LESLEY",
    "LINDSAY",
    "LLOYD",
    "LOCKWOOD",
    "LOUISE",
    "LYNNE",
    "MARGARET",
    "MARIA",
    "MARIAN",
    "MARIANNE",
    "MARIE",
    "MARK",
    "MARTIN",
    "MARY",
    "MATTHEW",
    "MAURICE",
    "MAX",
    "MEGAN",
    "MICHAEL",
    "MIKE",
    "MILES",
    "MURRAY",
    "NANCY",
    "NANDOR",
    "NATHAN",
    "NEIL",
    "NEVILLE",
    "NICHOLAS",
    "NICK",
    "NIGEL",
    "PAUL",
    "PETER",
    "PHIL",
    "PHILIP",
    "POTO",
    "RACHEL",
    "RALPH",
    "RAYMOND",
    "REUBEN",
    "RICHARD",
    "ROBERT",
    "ROBIN",
    "RODNEY",
    "ROGER",
    "RON",
    "RONALD",
    "ROSS",
    "ROY",
    "RUSSELL",
    "RUTH",
    "RYAN",
    "SAM",
    "SANDRA",
    "SARAH",
    "SHANE",
    "SHARON",
    "SIMON",
    "STEPHEN",
    "STEVE",
    "STEVEN",
    "STEWART",
    "SUE",
    "SUZANNE",
    "TAMATHA",
    "TIMOTHY",
    "TIM",
    "TODD",
    "TONY",
    "TREVOR",
    "VANESSA",
    "VAUGHAN",
    "VIRGINIA",
    "VUI",
    "WARREN",
    "WAYNE",
    "WILLIAM",
    "WINSTON",
    "WYATT",
}

# NZ Parliament former-members URL pattern for placeholder authority URLs.
FORMER_MEMBERS_URL_TEMPLATE = (
    "https://www3.parliament.nz/en/mps-and-electorates/former-members-of-parliament/{slug}/"
)


def _nfkd(value: str) -> str:
    """Apply Unicode NFKD normalization and strip combining marks (macrons → ASCII: Tāmati → Tamati)."""
    nfkd = unicodedata.normalize("NFKD", value)
    # Strip combining diacritical marks (U+0300–U+036F) that NFKD introduces
    return "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_triangulated_authority() -> dict[str, Any] | None:
    """Load triangulated authority if available, otherwise return None.
    
    Triangulation cross-references auto-derived records against Wikidata
    to enrich them with official IDs, party labels, and service periods.
    """
    if TRIANGULATED_PATH.exists():
        data = _load_json(TRIANGULATED_PATH)
        triangulation = data.get("triangulation", {})
        matched = triangulation.get("matched_count", 0)
        total = triangulation.get("auto_derived_count", 0)
        print(f"  Using triangulated authority ({matched}/{total} records matched vs Wikidata)")
        return data
    print("  Triangulated authority not found; using auto-derived only.")
    return None


def _member_id(local_key: str) -> str:
    payload = component_payload(
        release_version="0.1.0",
        component_type="member",
        source_stable_id="nz-parliament-corpus-derived",
        local_key=local_key,
        validation_manifest="manifests/corpus_wide_member_identity_validation.json",
    )
    return canonical_id("neutral-component", payload)


def extract_tokens() -> Counter[str]:
    tbl = pq.read_table(PARQUET_PATH, columns=["member_of_parliament_raw"])
    raws = [r for r in tbl.column("member_of_parliament_raw").to_pylist() if r]
    tokens: Counter[str] = Counter()
    for raw in raws:
        for part in raw.split(";"):
            tokens[part.strip()] += 1
    return tokens


def _detect_reversed_name(name: str) -> str | None:
    """Detect and fix reversed names like 'Foster-Bell Paul' -> 'Paul Foster-Bell'.

    Returns the corrected name if detected, or None if the name appears normal.
    """
    parts = name.split()
    if len(parts) < 2:
        return None
    last_word_upper = parts[-1].upper()
    if last_word_upper in KNOWN_FIRST_NAMES:
        return " ".join([parts[-1]] + parts[:-1])
    return None


def _generate_authority_url(canonical_name: str) -> str:
    """Generate a placeholder authority URL using the NZ Parliament former-members pattern."""
    norm = _normalize_token(canonical_name).strip()
    if not norm:
        return ""
    words = norm.lower().split()
    if len(words) == 1:
        slug = words[0]
    else:
        slug = "-".join([words[-1]] + words[:-1])
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    if not slug:
        return ""
    return FORMER_MEMBERS_URL_TEMPLATE.format(slug=slug)


def _merge_near_duplicates(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Merge records that are near-duplicates differing only by a middle name.

    For example, 'Hilary Jane Calvert' and 'Hilary Calvert' are merged into
    one record with the longer form as canonical and the shorter as an alias.
    """
    if not records:
        return records

    # Build index by surname (last word) for grouping
    surname_groups: dict[str, list[dict[str, Any]]] = {}
    for rec in records:
        norm = _normalize_token(rec["canonical_name"]).upper()
        words = norm.split()
        if words:
            surname = words[-1]
            surname_groups.setdefault(surname, []).append(rec)
        else:
            key = f"__no_surname_{id(rec)}"
            surname_groups.setdefault(key, []).append(rec)

    merged: list[dict[str, Any]] = []
    for surname, group in surname_groups.items():
        if len(group) < 2:
            merged.extend(group)
            continue

        # Group records within same surname by first word (given name)
        first_name_groups: dict[str, list[dict[str, Any]]] = {}
        for rec in group:
            norm = _normalize_token(rec["canonical_name"]).upper()
            words = norm.split()
            given = words[0] if words else ""
            compound_key = f"{given}|{surname}"
            first_name_groups.setdefault(compound_key, []).append(rec)

        for fng_key, fng in first_name_groups.items():
            if len(fng) < 2:
                merged.extend(fng)
                continue

            # Sort by word count ascending so shorter -> longer
            fng.sort(key=lambda r: len(_normalize_token(r["canonical_name"]).split()))

            # Longest = canonical, shorter ones become aliases
            longest = fng[-1]
            merged_aliases = list(longest.get("aliases", []))
            for shorter in fng[:-1]:
                short_canonical = shorter["canonical_name"]
                if short_canonical != longest["canonical_name"]:
                    merged_aliases.append(short_canonical)
                for alias in shorter.get("aliases", []):
                    if alias != longest["canonical_name"] and alias not in merged_aliases:
                        merged_aliases.append(alias)

            canonical = longest["canonical_name"]
            local_key = re.sub(r"[^a-z0-9]+", "-", canonical.lower()).strip("-")
            mid = _member_id(local_key)
            merged.append(
                {
                    "component_id": mid,
                    "member_id": mid,
                    "display_name": canonical,
                    "canonical_name": canonical,
                    "aliases": merged_aliases,
                    "authority_source_id": "nz-parliament-corpus-derived",
                    "authority_url": _generate_authority_url(canonical),
                    "service_periods": [],
                    "resolution_scope": "corpus-auto-derived",
                }
            )

    return merged


def build_authority(tokens: Counter[str]) -> dict[str, Any]:
    # First pass: group by NFKD-normalized + honorific-stripped key
    # This merges macron variants (Tāmati → Tamati) and honorific variants
    groups: dict[str, list[tuple[str, int]]] = {}
    for token, count in tokens.most_common():
        if token in IGNORED_TOKENS:
            continue
        normalized = _normalize_token(token).upper()
        nfkd_normalized = _nfkd(normalized)
        if not nfkd_normalized:
            continue
        if len(nfkd_normalized) < MIN_TOKEN_LENGTH:
            continue
        groups.setdefault(nfkd_normalized, []).append((token, count))

    member_records: list[dict[str, Any]] = []
    for nfkd_key, variants in groups.items():
        variants.sort(key=lambda x: -x[1])
        # Use honorific-stripped NFKD-normalized form as canonical, with original casing
        # Recover proper name case from the most common variant
        most_common_raw = variants[0][0]
        canonical_norm = _normalize_token(most_common_raw)
        if not canonical_norm:
            canonical_norm = nfkd_key.title()
        aliases = []
        seen_aliases = set()
        for v, _ in variants[1:]:
            raw_v = v
            if raw_v != most_common_raw and raw_v not in seen_aliases:
                aliases.append(raw_v)
                seen_aliases.add(raw_v)
            # Also add honorific-stripped variant if different from canonical
            stripped_v = _normalize_token(v)
            if stripped_v != canonical_norm and stripped_v not in seen_aliases:
                aliases.append(stripped_v)
                seen_aliases.add(stripped_v)
        local_key = re.sub(r"[^a-z0-9]+", "-", canonical_norm.lower()).strip("-")
        mid = _member_id(local_key)
        member_records.append(
            {
                "component_id": mid,
                "member_id": mid,
                "display_name": canonical_norm,
                "canonical_name": canonical_norm,
                "aliases": aliases,
                "authority_source_id": "nz-parliament-corpus-derived",
                "authority_url": _generate_authority_url(canonical_norm),
                "service_periods": [],
                "resolution_scope": "corpus-auto-derived",
            }
        )

    # Filter out known non-MP records
    member_records = [r for r in member_records if r["canonical_name"] not in IGNORED_TOKENS]

    # Apply reversed-name detection to each record's canonical name
    for rec in member_records:
        corrected = _detect_reversed_name(rec["canonical_name"])
        if corrected:
            old_canonical = rec["canonical_name"]
            rec["canonical_name"] = corrected
            rec["display_name"] = corrected
            if old_canonical not in rec["aliases"]:
                rec["aliases"].append(old_canonical)
            local_key = re.sub(r"[^a-z0-9]+", "-", corrected.lower()).strip("-")
            mid = _member_id(local_key)
            rec["component_id"] = mid
            rec["member_id"] = mid
            rec["authority_url"] = _generate_authority_url(corrected)

    # Merge near-duplicates differing only by middle name
    member_records = _merge_near_duplicates(member_records)

    return {
        "track_id": "corpus_wide_member_identity_release_20260610",
        "generated_at": "2026-06-12",
        "purpose": "Corpus-wide member identity authority table auto-derived from unique member tokens in the Hansard corpus.",
        "source_hashes": {
            "hansard_parquet": _sha256_path(PARQUET_PATH),
        },
        "authority_sources": [
            {
                "authority_source_id": "nz-parliament-corpus-derived",
                "title": "Corpus-wide member identity (auto-derived)",
                "url": "",
                "publisher": "Auto-derived from corpus-nz-hansard",
                "coverage_note": "Member records auto-extracted from unique member_of_parliament_raw tokens. Service periods are not verified. Human review required before validated release.",
                "source_hash": _sha256_path(PARQUET_PATH),
            },
        ],
        "resolution_rules": [
            "Member records are auto-derived from unique name tokens found in the corpus.",
            "Honorifics such as Hon, Rt Hon, Dr, Sir, Dame, Mr, Mrs, Ms, Miss, and Prof are stripped before normalization.",
            "Semicolon-delimited raw member values are split into separate tokens.",
            "The most common variant of each normalized name becomes the canonical form.",
            "All less-common variants become aliases.",
            "Reversed name tokens (e.g. 'Foster-Bell Paul') are detected and corrected to 'Paul Foster-Bell'.",
            "Near-duplicate records differing only by middle name (e.g. 'Hilary Jane Calvert' vs 'Hilary Calvert') are merged.",
            "Placeholder authority URLs using the NZ Parliament former-members URL pattern are generated for each record.",
            "This authority is auto-derived and NOT yet human-validated against official sources.",
            "Service periods, official IDs, and authority URLs are not populated.",
        ],
        "member_records": member_records,
        "review_notes": [
            "Auto-derived authority from corpus member tokens. Not yet reviewed against official NZ Parliament sources.",
            "Release remains blocked-pending-authority-coverage-review until human validation is complete.",
            "Service periods, authority URLs, and official member IDs require web scraping or manual data entry.",
        ],
    }


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    # Try loading triangulated authority first (enriched via Wikidata cross-reference)
    triangulated = load_triangulated_authority()
    if triangulated is not None:
        # Filter out known non-MP records before writing
        records = triangulated.get("member_records", [])
        filtered = [r for r in records if r.get("canonical_name", "") not in IGNORED_TOKENS]
        if len(filtered) < len(records):
            print(f"  Filtered out {len(records) - len(filtered)} known non-MP records")
            triangulated["member_records"] = filtered
        n_records = len(triangulated["member_records"])
        AUTHORITY_PATH.parent.mkdir(parents=True, exist_ok=True)
        AUTHORITY_PATH.write_text(
            json.dumps(triangulated, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"  Wrote triangulated authority to {AUTHORITY_PATH}")
        print(f"  {n_records} records")
        return 0

    print("Extracting unique member tokens from corpus...")
    tokens = extract_tokens()
    print(f"  Raw unique tokens: {len(tokens)}")
    total = sum(tokens.values())
    print(f"  Total token occurrences: {total}")

    authority = build_authority(tokens)
    n_records = len(authority["member_records"])
    print(f"  Generated {n_records} member authority records")

    AUTHORITY_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUTHORITY_PATH.write_text(
        json.dumps(authority, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"  Wrote {AUTHORITY_PATH}")

    # Summary
    resolved = sum(1 for r in authority["member_records"] if r["aliases"])
    print(f"  Records with aliases: {resolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
