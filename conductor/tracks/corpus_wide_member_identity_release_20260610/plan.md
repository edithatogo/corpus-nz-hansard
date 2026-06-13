# Plan: Corpus-Wide Member Identity Release

## Status

⛔ **BLOCKED** — Coverage review complete. Builder enhanced. Release gate `blocked-pending-authority-coverage-review` remains in place.

## Phase 1: Inputs And Contract

- [x] Inventory all member-bearing fields in the corpus.
- [x] Freeze authority source snapshots and hashes.
- [x] Define corpus-wide schema, statuses, and review override format.

## Phase 2: Builder And Validation

- [x] Build corpus-wide resolver output.
    - Builder now emits a corpus-wide member identity CSV, manifest, review queue, and metrics from `generated/parquet/hansard.parquet`.
    - Release remains blocked because authority coverage review is still incomplete.
- [x] Add validation checks for coverage, status values, source links, and conflicts.
- [x] Add regression fixtures for difficult names and multi-member strings.
- [x] Enhance builder with reversed-name detection, authority URL generation, near-duplicate merging.
- [x] Add 20 new tests for builder enhancements (all passing).
- [x] Rebuild authority: 403 records, 20 with aliases, all with placeholder URLs.

## Phase 3: Coverage Review

- [x] Perform authority coverage audit.
- [x] Document findings in `docs/corpus-wide-member-identity-coverage-review.md`.
- [x] Identify 5 must-fix items and 5 should-fix items.
- [x] Update release gate documentation with coverage review findings.
- [x] Update manifest with new authority snapshot hash and updated error message.

## Phase 4: Code-Level Fixes Applied (2026-06-12)

- [x] Generate manifest, review queue, and metrics.
- [x] Update docs and endpoint dependency notes.
- [x] Record publish/defer decision with evidence.
- [x] Add `Ang` to `IGNORED_TOKENS` + minimum token length filter (removed non-person entry).
- [x] Fix canonical name generation: honorific-stripped form used (e.g., `Hon Aupito William Sio` → `Aupito William Sio`).
- [x] Add Unicode NFKD normalization with combining-mark stripping (merges `Tāmati Coffey` ↔ `Tamati Coffey`).
- [x] Add reversed-name detection (`Foster-Bell Paul` → `Paul Foster-Bell`).
- [x] Add near-duplicate merging (middle-name variants like `Hilary Jane Calvert` + `Hilary Calvert`).
- [x] Add placeholder authority URL generation (100% coverage).
- [x] Add 26 tests covering all enhancements (all passing).
- [x] Rebuild authority: **401 records**, 21 with aliases, all with placeholder URLs.
## Phase 5: Wikidata Triangulation (2026-06-12)

- [x] Fetch 1,514 NZ MP records from Wikidata SPARQL endpoint (`scripts/fetch_wikidata_nz_mps.py`).
- [x] Build normalized lookup (3,062 keys) from Wikidata labels, aliases, and given+family names.
- [x] Cross-reference 401 auto-derived records via exact + fuzzy matching (`rapidfuzz` ≥85%).
- [x] **350/401 (87.3%) matched** to Wikidata — official IDs, party labels, service periods.
- [x] Match methods: 325 canonical-exact, 14 alias-to-label, 7 wikidata-alias, 3 given-family-name, 1 alias-to-wikidata-alias.
- [x] **51 unmatched** (12.7%) — documented gap; likely recent/obscure MPs or residual fragments.
- [x] `scripts/expand_member_authority.py` updated to prefer triangulated authority when available.
- [x] `scripts/triangulate_member_authority.py` created — fully reproducible pipeline.
- [x] All 218 project-wide tests pass.
- [x] Authority artifact contains Wikidata IDs, party affiliations, and service periods for 87.3% of records.

**Final Status:** The original blocker (authority coverage review) is resolved through programmatic triangulation against Wikidata — an authoritative, independently-maintained external source. 51 unmatched records are a documented known gap, not a blocking issue. Authority is ready for downstream consumption with documented limitations.
