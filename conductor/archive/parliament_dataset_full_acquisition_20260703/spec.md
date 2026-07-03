# Specification: Parliament Dataset Full Acquisition

## Overview

Implement repeatable, resumable, rights-safe full acquisition for approved Parliament website dataset families after the inventory and seed-fetcher tracks have validated source posture and retrieval feasibility.

This track depends on completed `parliament_dataset_inventory_20260703` and `parliament_dataset_seed_fetchers_20260703` evidence.

## Functional Requirements

- Design a cache and acquisition layout for approved sources, including raw snapshots, normalized indexes, manifests, and validation reports.
- Implement full acquisition builders for sources approved by the inventory and proven by seed fetchers, especially:
  - Journals and related index surfaces.
  - Papers presented/current papers/AJHR handoff records.
  - Order Papers, questions, business statements, and Daily Progress.
  - Select committee reports, submissions/advice, meetings, submitters, and videos where accessible.
  - Petitions.
  - Members, former members, parties, seating, and contact/office downloads.
  - Parliament video/audio/calendar metadata where accessible.
- Add full acquisition manifests with source IDs, coverage windows, counts, hashes, cache paths, blocked records, retry/error summaries, refresh cadence, and rights boundaries.
- Add cross-source reconciliation checks for journals, papers, questions, committees, petitions, and members.
- Integrate full-acquisition validation into quality gates without requiring live network access during normal CI.

## Non-Functional Requirements

- Acquisition must be resumable and bounded by explicit target/source selection.
- All outputs must be hash-backed and regenerable.
- Rights and public-claim boundaries must prevent accidental publication overclaims.
- HathiTrust and Internet Archive must not be acquisition dependencies.
- NZ legislation and Gazette remain excluded.

## Acceptance Criteria

- Full acquisition can run for approved targets and produce validated manifests.
- Checkers fail on missing hashes, unbounded outputs, missing coverage statements, missing rights boundaries, or excluded-source leakage.
- Mocked tests cover fetch, cache, resume, blocked-source, and reconciliation behavior.
- Documentation describes operator commands, cache policy, refresh cadence, and publication/readiness status.

## Out of Scope

- Acquisition from HathiTrust or Internet Archive.
- NZ legislation or Gazette acquisition.
- Public release unless a later publication track explicitly promotes artifacts.
- Manual scraping that bypasses legal or technical access constraints.
