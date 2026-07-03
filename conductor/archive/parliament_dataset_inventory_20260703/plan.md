# Plan: Parliament Dataset Inventory

## Phase 1: Dataset Taxonomy And Boundaries

- [x] Task: Confirm the in-scope dataset families and explicit exclusions.
    - [x] Review existing authority-source, historical sitting, and cross-repo architecture artifacts.
    - [x] Record exclusion rules for NZ legislation, Gazette, HathiTrust, and Internet Archive.
- [x] Task: Define source classifications and acquisition-priority vocabulary.
    - [x] Include official, fallback, supporting, and evidence-only source postures.
    - [x] Define how fallback sources relate to official Parliament records.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Dataset Taxonomy And Boundaries' (Protocol in workflow.md)
    - Automated/manual-equivalent evidence: `docs/parliament-dataset-inventory.md` records the in-scope families, exclusions, posture vocabulary, and fallback relationship rules.

## Phase 2: Inventory Manifest And Schema

- [x] Task: Write schema-first tests for the Parliament dataset inventory.
    - [x] Test required source fields, duplicate ID rejection, source posture validation, and exclusion policy.
    - [x] Test that NZ legislation and Gazette remain excluded.
- [x] Task: Implement the inventory schema and manifest.
    - [x] Add dataset-family records for all in-scope Parliament website families.
    - [x] Add credible fallback-source records for Papers Past/NLNZ, Google Books, library holdings, O Nehera/Waikato, and Data.govt.nz evidence-only requests.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Inventory Manifest And Schema' (Protocol in workflow.md)
    - Automated/manual-equivalent evidence: `pixi run python -m pytest -q tests\test_parliament_dataset_inventory.py` passed.

## Phase 3: Checker And Documentation

- [x] Task: Add a checker for the inventory manifest.
    - [x] Validate schema, official-first posture, fallback classifications, exclusions, and no completeness overclaims.
    - [x] Integrate the checker into the documented quality lane if appropriate.
- [x] Task: Add inventory documentation.
    - [x] Explain source families, fallback-source posture, known access constraints, and handoff to the seed-fetcher track.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Checker And Documentation' (Protocol in workflow.md)
    - Automated/manual-equivalent evidence: `pixi run python scripts\check_parliament_dataset_inventory.py`, `pixi run python scripts\check_quality_gate.py`, `pixi run lint`, and `pixi run format-check` passed.

## Phase 4: Reconciliation And Handoff

- [x] Task: Reconcile the inventory with existing authority-source and cross-repo artifacts.
    - [x] Confirm no conflict with `manifests/authority_sources.json`.
    - [x] Confirm no conflict with historical sitting inventory and legislation-repo boundaries.
- [x] Task: Create seed-fetcher handoff requirements.
    - [x] Identify priority seed targets and expected proof artifacts for the next track.
- [x] Task: Run validation.
    - [x] Run the new checker.
    - [x] Run focused tests and the repository quality/test commands required by the track.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Reconciliation And Handoff' (Protocol in workflow.md)
    - Automated/manual-equivalent evidence: the manifest checker validates references to `authority_sources.json`, `historical_sitting_inventory.json`, and `docs/cross-repo-dataset-architecture.md`, plus handoff requirements for `parliament_dataset_seed_fetchers_20260703`.
