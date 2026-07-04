# Historical Coverage Breadth Integration

## Overview

Build a cross-repo historical coverage reconciliation layer for New Zealand Parliament publication coverage. The goal is to improve historical completeness and breadth without claiming completeness, by treating this repo's Parliament website inventory as the primary scope and adjacent repositories as evidence and boundary inputs.

This track is intentionally cross-repo:
- `corpus-nz-hansard` provides the Parliament website inventory, boundary rules, and official-first dataset posture.
- `hathi-nz` provides HathiTrust-side historical Hansard discovery and archive evidence.
- `corpus-law-nz` remains the legislation/Gazette boundary reference and is not an acquisition target here.

## Functional Requirements

1. Define a family-level historical coverage model for Parliament datasets that separates official, fallback, supporting, excluded, and evidence-only sources.
2. Add a machine-readable reconciliation manifest that records historical gaps, adjacent-repo evidence pointers, and the no-completeness-claim posture.
3. Record how HathiTrust, Papers Past, Google Books, library catalogues, and other supporting sources help detect or narrow historical gaps.
4. Preserve the current exclusions for NZ legislation and the Gazette, with explicit references to the adjacent repo boundary.
5. Add validation so fallback sources cannot be promoted to primary sources without a deliberate manifest change.
6. Update cross-repo documentation so the integration path is visible from both the Parliament repo and the adjacent source repositories.

## Non-Functional Requirements

- Keep the workflow deterministic and hash-backed.
- Do not introduce bulk-acquisition dependencies.
- Do not claim historical completeness.
- Keep all outputs reproducible from tracked source manifests and adjacent repo references.

## Acceptance Criteria

- The reconciliation manifest validates against its schema.
- The docs describe the cross-repo boundary and the historical gap model.
- Tests verify source classification, exclusion handling, and fallback-source handling.
- The repo still clearly distinguishes discovery evidence from acquisition evidence.

## Out of Scope

- Bulk acquisition from HathiTrust or other historical repositories.
- Any NZ legislation or Gazette acquisition work.
- Publishing a historical-completeness claim.
- Changing adjacent repos' acquisition flows as part of this track.
