# Spec: Release Hosting and Versioning

## Goal

Create local release/versioning artifacts for review without uploading, publishing, or changing generated corpus data.

## Required Outputs

- Version file.
- Release notes.
- Hosting decision matrix.
- Local release package builder.
- Machine-readable release package manifest.
- Tests for package manifest and packaging behavior.
- Evidence proving no upload/publication occurred.

## Acceptance Criteria

- Version identifier is explicit.
- Release notes distinguish local review packaging from public release.
- Package excludes source ZIP and large generated corpus outputs by default.
- Package includes docs, manifests, scripts, tests, Conductor evidence, and checksums.
- Generated package is written under ignored `generated/release/`.
- Tests pass and package manifest parses as JSON.

## Non-Goals

- No upload to any host.
- No Git tag or commit.
- No generated Parquet/DuckDB upload package unless explicitly requested later.
