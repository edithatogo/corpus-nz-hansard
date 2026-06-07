# Spec: Public Dataset Readiness

## Goal

Prepare release-facing documentation and manifests so the generated Hansard corpus can be reviewed for public dataset publication without yet uploading or publishing it.

## Required Outputs

- Dataset card.
- Licensing and provenance note with official source references.
- Public release checklist.
- Machine-readable public dataset release manifest.
- Tests for release manifest generation.
- Evidence tying release claims to existing inventory, schema, normalization, and DuckDB validation.

## Acceptance Criteria

- Documentation distinguishes copyright/provenance facts from publication decisions.
- Dataset card does not claim official endorsement.
- Manifest records source archive hash, row counts, generated outputs, warnings, and known limitations.
- Release-readiness status is explicit and does not imply publication has occurred.
- Existing generated corpus outputs are not moved or uploaded.

## Non-Goals

- No upload to Hugging Face, Zenodo, OSF, GitHub Releases, or another host.
- No legal advice or final licensing sign-off.
- No compression of the full generated dataset into a release archive.
