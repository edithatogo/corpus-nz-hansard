# Evidence: Artifact Provenance And Attestations

## Initial Evidence

Status: opened on 2026-06-09.

This track implements the corpus-family bleeding-edge versioning, CI/CD, code-quality, automation, and provenance standard.

## Zenodo Archive Attestation - 2026-06-09

Repo-side hardening applied:

- Added GitHub artifact attestation permissions to `.github/workflows/zenodo_archive.yml`: `attestations: write`, `contents: read`, and `id-token: write`.
- Added `actions/attest-build-provenance` v4.1.0 pinned to commit `a2bbfa25375fe432b6a289bc6b6cd05ecd0c4c32`.
- Attestation subjects are the generated Zenodo archive tarball and manifest files: `generated/zenodo/*.tar.gz` and `generated/zenodo/*.manifest.json`.

Verification:

- Latest official `actions/attest-build-provenance` release was checked on 2026-06-09; `v4.1.0` was published on 2026-02-26.
- The pinned action metadata was inspected to confirm the `subject-path` input.
