# Plan: Parliament Dataset Inventory

## Phase 1: Dataset Taxonomy And Boundaries

- [ ] Task: Confirm the in-scope dataset families and explicit exclusions.
    - [ ] Review existing authority-source, historical sitting, and cross-repo architecture artifacts.
    - [ ] Record exclusion rules for NZ legislation, Gazette, HathiTrust, and Internet Archive.
- [ ] Task: Define source classifications and acquisition-priority vocabulary.
    - [ ] Include official, fallback, supporting, and evidence-only source postures.
    - [ ] Define how fallback sources relate to official Parliament records.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Dataset Taxonomy And Boundaries' (Protocol in workflow.md)

## Phase 2: Inventory Manifest And Schema

- [ ] Task: Write schema-first tests for the Parliament dataset inventory.
    - [ ] Test required source fields, duplicate ID rejection, source posture validation, and exclusion policy.
    - [ ] Test that NZ legislation and Gazette remain excluded.
- [ ] Task: Implement the inventory schema and manifest.
    - [ ] Add dataset-family records for all in-scope Parliament website families.
    - [ ] Add credible fallback-source records for Papers Past/NLNZ, Google Books, library holdings, O Nehera/Waikato, and Data.govt.nz evidence-only requests.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Inventory Manifest And Schema' (Protocol in workflow.md)

## Phase 3: Checker And Documentation

- [ ] Task: Add a checker for the inventory manifest.
    - [ ] Validate schema, official-first posture, fallback classifications, exclusions, and no completeness overclaims.
    - [ ] Integrate the checker into the documented quality lane if appropriate.
- [ ] Task: Add inventory documentation.
    - [ ] Explain source families, fallback-source posture, known access constraints, and handoff to the seed-fetcher track.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Checker And Documentation' (Protocol in workflow.md)

## Phase 4: Reconciliation And Handoff

- [ ] Task: Reconcile the inventory with existing authority-source and cross-repo artifacts.
    - [ ] Confirm no conflict with `manifests/authority_sources.json`.
    - [ ] Confirm no conflict with historical sitting inventory and legislation-repo boundaries.
- [ ] Task: Create seed-fetcher handoff requirements.
    - [ ] Identify priority seed targets and expected proof artifacts for the next track.
- [ ] Task: Run validation.
    - [ ] Run the new checker.
    - [ ] Run focused tests and the repository quality/test commands required by the track.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Reconciliation And Handoff' (Protocol in workflow.md)
