# Evidence: Release Ladder

## Release Levels

- Added `manifests/release_ladder.json`.
- Added `schemas/release_ladder.schema.json`.
- Defined five release levels: `document-level`, `authority-source`, `neutral-component`, `endpoint`, and `upstream-contribution`.
- Preserved `v0.1.0` as the immutable `document-level` public release except metadata, documentation, cross-reference, and provenance corrections that do not alter public rows, columns, source hashes, or intended use.

## Artifact Map

- Mapped current document-level release artifacts to `document-level`.
- Mapped `manifests/authority_sources.json` to `authority-source`.
- Mapped `docs/component-contracts.md` and candidate speech-turn outputs to `neutral-component`, with candidates still excluded.
- Mapped endpoint contracts and generated metadata packages to `endpoint`.
- Mapped upstream contribution planning to `upstream-contribution`.

## Manifest Fields

- Added release-series requirements to `docs/component-contracts.md`.
- Added endpoint release-series requirements to `docs/endpoint-contracts.md`.
- Required `release_series_id`, `release_level`, `artifact_name`, `artifact_version`, `input_release_versions`, `validation_manifest`, `publication_target`, `known_exclusions`, `release_status`, and `manifest_sha256`.

## Publication Docs

- Updated `docs/release-ladder.md`, `docs/public-release-checklist.md`, `docs/publication-status.md`, and `README.md`.
- Added `scripts/check_release_ladder.py` and `tests/test_release_ladder.py`.
- Wired the checker into `Makefile`, `.github/workflows/quality.yml`, `scripts/check_quality_gate.py`, and `docs/quality-gate.md`.

## Focused Validation

- `python scripts\check_release_ladder.py`
- `python -m unittest tests.test_release_ladder`
