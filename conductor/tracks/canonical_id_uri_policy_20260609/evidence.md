# Evidence: Canonical ID and URI Policy

## ID Patterns

- Added `manifests/id_uri_policy.json`.
- Added `schemas/canonical_id_uri_policy.schema.json`.
- Added `scripts/canonical_ids.py` for deterministic hash-backed ID and URI generation.
- Reused published document-level `stable_id` where document identity is sufficient.
- Forbid future neutral-component and endpoint IDs that depend on transient file paths or row positions alone.

## URI Namespace

- Added `docs/canonical-id-uri-policy.md`.
- Defined planned namespace `https://w3id.org/nz-hansard/`.
- Added URI patterns for document, component, endpoint, authority, and sample resources.
- Added SPARQL-friendly namespace guidance for RDF and linked metadata outputs.

## Deprecation Policy

- Required `manifests/id_uri_deprecations.json` before any published ID or URI replacement.
- Defined minimum mapping fields and redirect/tombstone expectations.

## Endpoint References

- Updated `docs/component-contracts.md`, `docs/endpoint-contracts.md`, `docs/shared-nz-corpus-core-schema.md`, `README.md`, and `manifests/release_ladder.json`.
- Wired `scripts/check_canonical_id_uri_policy.py` into `Makefile`, `.github/workflows/quality.yml`, `scripts/check_quality_gate.py`, and `docs/quality-gate.md`.

## Focused Validation

- `python scripts\check_canonical_id_uri_policy.py`
- `python -m unittest tests.test_canonical_id_uri_policy`
