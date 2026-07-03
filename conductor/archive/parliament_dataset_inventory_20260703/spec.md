# Specification: Parliament Dataset Inventory

## Overview

Create a validated inventory of Parliament-hosted and credible fallback datasets that can extend `corpus-nz-hansard` beyond the current DocumentsDB Hansard release, excluding NZ legislation and the Gazette because those are handled by the adjacent legislation corpus.

This track is discovery and governance only. It must not implement bulk downloaders or claim acquisition completeness.

## Functional Requirements

- Define a dataset-family taxonomy covering:
  - Hansard/debates.
  - Order Papers, oral questions, written questions, business statements, and the sitting programme.
  - Daily Progress in the House.
  - Journals: weekly, sessional, indexes, historic journals, and related journal surfaces.
  - Papers presented, current papers, and AJHR/Appendix material.
  - Select committee reports, submissions/advice, meetings, submitters, and videos.
  - Petitions.
  - MPs, former MPs, parliamentary parties, seating, and contact/office downloads.
  - Parliamentary rules and procedure.
  - Parliament video, audio, and calendar metadata.
- Record credible non-HathiTrust and non-Internet-Archive alternatives:
  - Papers Past / National Library.
  - Google Books.
  - University and library catalogues or physical holdings.
  - O Nehera / Waikato for British Parliamentary Papers context.
  - Data.govt.nz requests as evidence-only records, not acquisition sources.
- Add `manifests/parliament_dataset_inventory.json` with source IDs, dataset family, publisher, URL, source posture, access constraints, coverage period, refresh cadence, acquisition priority, fallback relationship, and explicit exclusion flags.
- Add `schemas/parliament_dataset_inventory.schema.json`, `scripts/check_parliament_dataset_inventory.py`, `tests/test_parliament_dataset_inventory.py`, and `docs/parliament-dataset-inventory.md`.
- Reconcile the inventory with existing `manifests/authority_sources.json`, `manifests/historical_sitting_inventory.json`, and `docs/cross-repo-dataset-architecture.md`.

## Non-Functional Requirements

- Official Parliament sources must be ranked before fallback or supporting sources.
- NZ legislation and Gazette records must be explicitly out of scope.
- HathiTrust and Internet Archive may be mentioned only as excluded or non-primary baselines.
- The inventory must not claim historical completeness unless a later acquisition/reconciliation track proves it.
- The checker must fail on missing source classifications, missing exclusion policy, duplicate source IDs, unsupported fallback classifications, or unbounded acquisition claims.

## Acceptance Criteria

- `pixi run python scripts/check_parliament_dataset_inventory.py` passes.
- `pixi run python -m pytest -q tests/test_parliament_dataset_inventory.py` passes.
- `docs/parliament-dataset-inventory.md` explains in-scope families, excluded families, fallback-source posture, and next-track handoff.
- Existing authority-source and cross-repo boundary docs remain consistent with the new inventory.

## Out of Scope

- Bulk acquisition.
- Seed fetchers or network retrieval beyond source-discovery evidence.
- Public release of newly inventoried datasets.
- NZ legislation or Gazette content.
- HathiTrust or Internet Archive acquisition.
