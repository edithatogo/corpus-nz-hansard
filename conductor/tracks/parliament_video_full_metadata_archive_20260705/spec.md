# Parliament Video Full Metadata Archive

## Overview

Scale from seed proofs to complete metadata capture for all approved NZ Parliament video surfaces, while keeping media files out of scope.

## Requirements

- Implement resumable metadata acquisition across all inventory-approved surfaces.
- Store normalized JSONL, source snapshots where allowed, request logs, hashes, counts, and blocked records.
- Add cache policy, retry/backoff, rate limiting, and deterministic IDs.
- Generate coverage and gap reports without claiming media archive completeness.

## Acceptance Criteria

- Full metadata archive manifest is repeatable and hash-backed.
- All approved surfaces are captured or explicitly blocked.
- Monthly refresh can update metadata without rewriting unresolved gaps.
