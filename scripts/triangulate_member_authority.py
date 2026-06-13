"""Triangulate auto-derived member authority against Wikidata and Parliament data."""
from __future__ import annotations
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any

try:
    from scripts.build_member_identity_review import _normalize_token
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_member_identity_review import _normalize_token

try:
    from rapidfuzz import fuzz
except ImportError:
    fuzz = None

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = ROOT / "derived/corpus_wide_member_identity_authority.json"
WIKIDATA_PATH = ROOT / "derived/wikidata_nz_mps.json"
PARLIAMENT_PATH = ROOT / "derived/parliament_current_mps.json"
OUTPUT_PATH = ROOT / "derived/triangulated_member_authority.json"

FUZZY_THRESHOLD = 85


def _nfkd(value: str) -> str:
    """Apply NFKD normalization and strip combining marks."""
    nfkd = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _norm(name: str) -> str:
    """Normalize a name for lookup: NFKD + honorific-strip + upper + strip."""
    return _nfkd(_normalize_token(name).upper().strip())


def _norm_without_initials(name: str) -> str:
    """Normalize and strip leading initials (e.g. 'H V Ross Robertson' -> 'ROSS ROBERTSON')."""
    n = _norm(name)
    parts = n.split()
    # Strip single-letter tokens at the start (initials like H, V, R)
    while parts and len(parts[0]) == 1 and parts[0].isalpha():
        parts.pop(0)
    return " ".join(parts) if parts else n


def _build_search_norms(record):
    """Build search norms including initial-stripped variants."""
    canonical = record.get("canonical_name", "") or ""
    aliases = record.get("aliases", []) or []
    search_names = [canonical] + list(aliases)
    norms = set()
    for n in search_names:
        if n and len(n) >= 3:
            nk = _norm(n)
            if len(nk) >= 3:
                norms.add(nk)
            # Also add initial-stripped variant
            nk2 = _norm_without_initials(n)
            if len(nk2) >= 3 and nk2 != nk:
                norms.add(nk2)
    return list(norms)


def _build_wikidata_lookup(wikidata):
    """Build a normalized lookup dict from Wikidata records."""
    lookup = {}
    for rec in wikidata.get("member_records", []):
        variants = set()
        label = rec.get("label", "") or ""
        if label:
            variants.add(label)
        for alias in rec.get("aliases", []):
            if alias:
                variants.add(alias)
        given = rec.get("given_name", "") or ""
        family = rec.get("family_name", "") or ""
        if given and family:
            variants.add(f"{given} {family}")
        for v in variants:
            nk = _norm(v)
            if len(nk) >= 3 and nk not in ("", "VACANT", "SPEAKER"):
                lookup.setdefault(nk, []).append(rec)
    return lookup


def _build_parliament_lookup(parliament_data):
    """Build a normalized lookup dict from Parliament current MPs data."""
    lookup = {}
    for rec in parliament_data.get("member_records", []):
        name = rec.get("name", "") or ""
        if name:
            nk = _norm(name)
            if len(nk) >= 3:
                lookup.setdefault(nk, []).append(rec)
    return lookup


def _match_record(record, lookup, source_records, id_field="wikidata_id"):
    """Match one auto-derived record against a source lookup."""
    search_norms = _build_search_norms(record)

    matched_ids = set()
    for norm_name in search_norms:
        candidates = lookup.get(norm_name, [])
        for c in candidates:
            matched_ids.add(c[id_field])

    if len(matched_ids) == 1:
        uid = next(iter(matched_ids))
        for sr in source_records:
            if sr[id_field] == uid:
                return sr

    if len(matched_ids) > 1:
        best, best_score = None, 0
        for uid in matched_ids:
            for sr in source_records:
                if sr[id_field] != uid:
                    continue
                label_norm = _norm(sr.get("label", "") or "")
                for norm_name in search_norms:
                    s = (fuzz.token_sort_ratio(norm_name, label_norm) if fuzz else (100 if norm_name == label_norm else 0))
                    if s > best_score:
                        best_score, best = s, sr
        if best and best_score >= FUZZY_THRESHOLD:
            return best

    if fuzz is None:
        return None
    for sr in source_records:
        label_norm = _norm(sr.get("label", "") or "")
        for norm_name in search_norms:
            s = fuzz.token_sort_ratio(norm_name, label_norm)
            if s >= FUZZY_THRESHOLD:
                return sr
            for alias in sr.get("aliases", []):
                if alias:
                    as_norm = _norm(alias)
                    if len(as_norm) >= 3:
                        s2 = fuzz.token_sort_ratio(norm_name, as_norm)
                        if s2 >= FUZZY_THRESHOLD:
                            return sr
    return None


def _get_match_method(record, wikidata_rec):
    canonical = record.get("canonical_name", "") or ""
    cn = _norm(canonical)
    ln = _norm(wikidata_rec.get("label", "") or "")
    if cn == ln:
        return "canonical-exact"
    given = wikidata_rec.get("given_name", "") or ""
    family = wikidata_rec.get("family_name", "") or ""
    if given and family and cn == _norm(f"{given} {family}"):
        return "given-family-name"
    for alias in (wikidata_rec.get("aliases", []) or []):
        if alias and cn == _norm(alias):
            return "wikidata-alias"
    for alias in (record.get("aliases", []) or []):
        if alias and _norm(alias) == ln:
            return "alias-to-label"
        for walias in (wikidata_rec.get("aliases", []) or []):
            if walias and _norm(alias) == _norm(walias):
                return "alias-to-wikidata-alias"
    return "fuzzy"


def _enrich_from_wikidata(rec, wd_rec):
    """Create enriched copy of record with Wikidata fields."""
    enriched_rec = dict(rec)
    method = _get_match_method(rec, wd_rec)
    enriched_rec["wikidata_id"] = wd_rec.get("wikidata_id", "")
    enriched_rec["wikidata_label"] = wd_rec.get("label", "")
    enriched_rec["wikidata_match_method"] = method
    if wd_rec.get("party"):
        enriched_rec["party"] = wd_rec["party"]
    if wd_rec.get("start_date") or wd_rec.get("end_date"):
        enriched_rec["service_periods"] = [{
            "start": wd_rec.get("start_date", ""),
            "end": wd_rec.get("end_date", ""),
        }]
    enriched_rec["resolution_scope"] = "triangulated-wikidata"
    enriched_rec["authority_source_id"] = "wikidata-nz-mps"
    enriched_rec["authority_url"] = f"https://www.wikidata.org/wiki/{wd_rec['wikidata_id']}"
    return enriched_rec


def _enrich_from_parliament(rec, parl_rec):
    """Create enriched copy of record with Parliament current MP fields."""
    enriched_rec = dict(rec)
    enriched_rec["parliament_nz_name"] = parl_rec.get("name", "")
    enriched_rec["parliament_nz_party"] = parl_rec.get("party", "")
    enriched_rec["resolution_scope"] = "triangulated-parliament"
    enriched_rec["authority_source_id"] = "parliament-nz-current"
    enriched_rec["authority_url"] = "https://www.parliament.nz/en/mps-and-electorates/members-of-parliament/"
    enriched_rec["wikidata_match_method"] = "parliament-nz-current"
    return enriched_rec


def main():
    print("Triangulating member authority against Wikidata and Parliament...")
    print(f"  Reading authority: {AUTHORITY_PATH}")
    authority = _load_json(AUTHORITY_PATH)
    auto_records = authority.get("member_records", [])
    print(f"  Auto-derived records: {len(auto_records)}")

    # === First pass: Wikidata matching ===
    print(f"  Reading Wikidata: {WIKIDATA_PATH}")
    wikidata = _load_json(WIKIDATA_PATH)
    wikidata_records = wikidata.get("member_records", [])
    print(f"  Wikidata MP records: {len(wikidata_records)}")
    wd_lookup = _build_wikidata_lookup(wikidata)
    print(f"  Wikidata lookup keys: {len(wd_lookup)}")

    wd_matched = 0
    wd_matched_ids = set()
    enriched = []
    for rec in auto_records:
        wd_rec = _match_record(rec, wd_lookup, wikidata_records)
        if wd_rec is not None:
            enriched_rec = _enrich_from_wikidata(rec, wd_rec)
            enriched.append(enriched_rec)
            wd_matched += 1
            wd_matched_ids.add(wd_rec.get("wikidata_id", ""))
        else:
            rec["resolution_scope"] = "corpus-auto-derived-unmatched"
            enriched.append(rec)

    # === Second pass: Parliament current MPs matching for unmatched records ===
    parl_matched = 0
    if PARLIAMENT_PATH.exists():
        print(f"\n  Second pass: Reading Parliament current MPs: {PARLIAMENT_PATH}")
        parliament = _load_json(PARLIAMENT_PATH)
        parliament_records = parliament.get("member_records", [])
        print(f"  Parliament current MP records: {len(parliament_records)}")
        parl_lookup = _build_parliament_lookup(parliament)
        print(f"  Parliament lookup keys: {len(parl_lookup)}")

        for i, rec in enumerate(enriched):
            if rec.get("resolution_scope") == "corpus-auto-derived-unmatched":
                parl_match = _match_record(rec, parl_lookup, parliament_records, id_field="name")
                if parl_match is not None:
                    enriched[i] = _enrich_from_parliament(rec, parl_match)
                    parl_matched += 1
        print(f"  Parliament-matched: {parl_matched}")
    else:
        print(f"\n  Parliament current MPs file not found at {PARLIAMENT_PATH}, skipping second pass.")

    # === Statistics ===
    total_matched = wd_matched + parl_matched
    by_method = {}
    for r in enriched:
        m = r.get("wikidata_match_method", "unmatched")
        by_method[m] = by_method.get(m, 0) + 1

    print(f"\n  Matched (Wikidata): {wd_matched}/{len(auto_records)}")
    if parl_matched:
        print(f"  Matched (Parliament): {parl_matched}/{len(auto_records)}")
    print(f"  Total matched: {total_matched}/{len(auto_records)}")
    print(f"  Match methods:")
    for m, c in sorted(by_method.items(), key=lambda x: -x[1]):
        print(f"    {m}: {c}")

    output = dict(authority)
    output["member_records"] = enriched
    output["triangulation"] = {
        "source": "wikidata+parliament",
        "wikidata_records_count": len(wikidata_records),
        "parliament_records_count": len(parliament_records) if PARLIAMENT_PATH.exists() else 0,
        "auto_derived_count": len(auto_records),
        "matched_count": total_matched,
        "unmatched_count": len(auto_records) - total_matched,
        "match_rate_pct": round(total_matched / len(auto_records) * 100, 1) if auto_records else 0,
        "wikidata_matched": wd_matched,
        "parliament_matched": parl_matched,
        "fuzzy_available": fuzz is not None,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT_PATH}")
    print(f"  {len(enriched)} records ({total_matched} triangulated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())