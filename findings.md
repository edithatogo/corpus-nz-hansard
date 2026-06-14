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

---

## Architect Oracle Analysis for Antigravity Subdirectory Swarm (2026-06-14)

### Swarm Context

This run is part of the **Antigravity subdirectory swarm** for `corpus-nz-hansard`. The swarm has 5 agents:
1. **architect_oracle** (me) — Architecture, root cause analysis
2. **general_coder** — Implementation work
3. **codex_gpt55_engineer** — AI-assisted engineering
4. **chrome_operator** — Browser automation (gated)
5. **quality_validator** — QA and testing

### Current State Assessment

The repository is in an advanced state with **64+ conductor tracks**, most completed (`[x]`). The active work is concentrated in:

**In Progress (`[~]`):**
1. **bills_api_integration_20260612** — Extraction done (3,513 bills, 351 member names); needs cross-referencing
2. **wikipedia_mp_lists_acquisition_20260612** — 249 MPs from Parl 52-53; 47-51 FAIL (older wikitable format)
3. **member_identity_triangulation_20260612** — 50/51 resolved (98%); 1 remaining (Laura Trask is non-MP)
4. **parliament_website_stealth_access_20260612** — All 5 targets fetched; Playwright script in place
5. **hathitrust_hansard_acquisition_20260612** — API discovery complete; pending OAuth key and Cloudflare bypass

**Blocked (`[!]`) — All depend on validated member identity:**
- Corpus-wide member identity release
- Corpus-wide party attribution release
- Validated speech-turn component release
- Sitting/proceeding component release
- Vote/motion/bill/question extraction
- All public endpoint releases (ParlaMint, Popolo, Akoma Ntoso, CAP, UD, RDF)
- Speech-act classifiers, NIF/RDF views, W3C Time, OntoLex, full historical reconciliation

### Critical Path Analysis

**The primary bottleneck** is `corpus_wide_member_identity_release_20260610`. Once unblocked, it cascades to unblock party attribution, speech-turn validation, and all 6+ endpoint tracks.

However — the member identity track has already been significantly advanced:
- 401 auto-derived records → 350 matched via Wikidata → 51 manually resolved via Wikipedia/Bills/manual (98%)
- Builder enhanced with reversed-name detection, near-duplicate merging, NFKD normalization
- Triangulation script complete and reproducible
- The 5 "must-fix" items from coverage review (`Ang`, honorifics, `Tamati/Tāmati`, near-duplicates, human validation) have been addressed

**The real remaining work is not code — it's human validation and documentation promotion.**

### Recommendations for This Swarm

1. **Local non-gated work that can be done now:**
   - Verify that the triangulation pipeline is fully reproducible
   - Update conductor track statuses to reflect actual completion
   - Check the `derived/crossref_bills_api.json` — Librarian noted `bills_api_members_count = 0`
   - Run any waiting builder/checker scripts to reprocess outputs
   - Review the `parliament_website_stealth_access_20260612` artifacts and extract member data from saved HTML

2. **Gated work (requires approval):**
   - HathiTrust OAuth key request
   - GitHub commit/push
   - Hugging Face / Zenodo publication
   - Chrome browser profile automation

3. **Architectural observations:**
   - The Wikidata SPARQL query has a systematic gap: P463 vs P39. Fixing this would auto-resolve ~35 of the previously 51 unmatched names without manual curation.
   - Wikipedia parsing for Parliaments 47-51 could use a fallback parser for older wikitable format.
   - The `fetch_bills_api.py` member extraction counts (351) should be cross-referenced with the 401 auto-derived records from the corpus.
   - Laura Trask is confirmed as Laura McClure (ACT) — a corpus error, not a resolution gap.
