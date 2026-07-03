# Specification: Parliament Dataset Seed Fetchers

## Overview

Implement safe, bounded seed fetchers for the highest-value dataset families identified by `parliament_dataset_inventory_20260703`. Seed fetchers prove retrieval feasibility and artifact shape without bulk acquisition or publication claims.

This track depends on a valid Parliament dataset inventory.

## Functional Requirements

- Select priority seed targets from the completed inventory, covering at minimum:
  - Journals.
  - Papers presented or AJHR/current papers.
  - Order Paper and questions.
  - Select committee reports/submissions/advice.
  - Petitions.
  - Members/parties/contact downloads.
- Add seed-fetcher scripts that retrieve one index page or API response plus one representative detail/sample artifact per target family where technically feasible.
- Write `manifests/parliament_dataset_seed_fetchers.json` with source IDs, request URLs, fetched timestamps, response hashes, record/sample counts, access constraints, source classification, and proof status.
- Add schema, checker, docs, and mocked network tests.
- Reuse the repo-local retry helper and avoid side effects beyond explicit generated/derived seed artifacts.

## Non-Functional Requirements

- Seed fetchers must be bounded, deterministic where possible, and safe to run in CI using mocked fixtures.
- No seed artifact may be described as complete, public-release-ready, or authoritative full acquisition.
- Fetchers must preserve source URLs, timestamps, content hashes, and access notes.
- Parliament official endpoints remain preferred; fallback sources are sampled only when the inventory marks them credible.

## Acceptance Criteria

- Seed-fetcher unit tests use mocked HTTP or fixture inputs.
- `pixi run python scripts/check_parliament_dataset_seed_fetchers.py` passes.
- Seed manifest records at least one feasible proof per approved priority family or an explicit blocked/deferred reason.
- Documentation explains how seed evidence will hand off to full acquisition.

## Out of Scope

- Bulk crawling or complete dataset acquisition.
- Publication to Hugging Face, Zenodo, OSF, or mirrors.
- NZ legislation and Gazette content.
- HathiTrust or Internet Archive acquisition.
