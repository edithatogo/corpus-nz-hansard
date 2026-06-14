# Findings & Scratchpad (Oracle Analysis)

Use this file to store shared knowledge, research notes, and intermediate outputs.


## Oracle Architectural Analysis (2026-06-14)

### 1. System Architecture

Member identity resolution is a multi-stage pipeline with five data-source integrations.

**Data Acquisition Layer:**
- Bills API (351 members, Parl 43-54)
- Wikipedia MP Lists (249 recs, Parl 52-53 only; 47-51 FAIL)
- Wikidata SPARQL (1,514 recs with provenance chains)
- Parliament Current MPs (123 recs, 54th Parliament curated)

**Corpus Extraction Layer** (scripts/expand_member_authority.py):
- Reads Hansard parquet (193,922 rows)
- Extracts unique member_of_parliament_raw tokens
- NFKD normalization + honorific stripping + reversed name detection
- Merges near-duplicates differing only by middle name
- Output: 401 auto-derived records

**Triangulation Layer** (scripts/triangulate_member_authority.py):
- Pass 1: Wikidata matching (exact + fuzzy token_sort_ratio >= 85)
- Pass 2: Parliament current MPs matching for unmatched records
- Output: 350 matched, 51 unmatched (87.3% match rate initially)

**Resolution Layer** (manual + create_member_registry.py):
- 41 via 54th Parliament Wikipedia, 5 via 47-53 manual, 4 via Wikidata, 1 via Bills API
- Output: member_registry.json (51/51 = 100%)

**Validation Layer:**
- check_authority_sources.py, check_member_identity_resolution.py


### 2. Root Cause Analysis of 51 Unmatched Names

Initial match rate: 87.3% (350/401) - 51 records unmatched against Wikidata/Parliament.

| Root Cause Category | Count | Examples |
|---|---|---|
| New 54th Parl MPs (no Wikidata P39) | ~35 | Kahurangi Carter, Scott Willis, Steve Abel, Lawrence Xu-Nan, Cameron Luxton -- 2023 MPs missing the P39 position statement |
| Macron/diacritic variants (NFKD clash) | 2 | Huhana Lyndon -> Huhana Lyndon; Takuta Ferris -> Takuta Ferris |
| Initial-prefixed names (no alias variant) | 2 | H V Ross Robertson -> Ross Robertson; R Doug Woolerton -> Doug Woolerton |
| Name ordering issue (corpus reversed) | 1 | Paul Tamatha -> Tamatha Paul |
| Typo/misspelling in source | 1 | Richard Posser -> Richard Prosser |
| Non-existent MP in corpus | 1 | Laura Trask -> Laura McClure (ACT) |
| Full-name vs short-name mismatch | 2 | Anahila Kanongata'a -> A. Kanongata'a-Suisuiki; Asenati Lole-Taylor -> Asenati Taylor |
| Name variants (Gerry/Gerrard) | 1 | Gerrard Eckhoff -> Gerry Eckhoff |

**Key Finding**: The Wikidata P39 query systematically misses ~35 MPs from 54th Parliament because their items use P463 (member of: NZ House of Reps) instead of P39. The fallback query uses FILTER NOT EXISTS which misses items that have NEITHER.
