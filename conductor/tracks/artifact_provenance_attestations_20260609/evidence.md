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
- Live non-upload archive verification succeeded on GitHub Actions run `27203903098` for commit `70b7870cc552297967297527dfe5056d7ef18e20`.
- In run `27203903098`, `Upload Zenodo draft` was skipped as intended, `Upload archive artifact` succeeded, and `Attest Zenodo archive provenance` succeeded.
- The workflow produced artifact `nz-hansard-zenodo-archive-0.1.0` with reported size `327428061` bytes and `expired: false` at verification time.
