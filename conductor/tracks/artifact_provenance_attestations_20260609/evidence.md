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

## Release Evidence Ledger And Policy Checks - 2026-06-09

Repo-side hardening applied:

- Added `schemas/release_evidence_ledger.schema.json` with required evidence for commit SHA, workflow run, Hugging Face revision, Zenodo DOI/concept DOI, manifests, artifacts, dataset schema version, record count, coverage statement, and provenance policy.
- Added `scripts/build_release_evidence_ledger.py` to emit a machine-readable ledger with SHA-256 and byte-size evidence for release manifests and artifacts.
- Added `docs/release-evidence-ledger.md` to map artifact classes to GitHub artifact attestation, revision-plus-manifest evidence, signed/checksummed artifacts, or documented deferral.
- Added `scripts/check_release_provenance_policy.py` and wired it into `.github/workflows/quality.yml` and `Makefile`.
- Documented the check in `docs/quality-gate.md`; dependency-update PRs remain unable to publish because publication workflows are manual-only and are checked by both quality and provenance policy guards.
- Renovate remains documented as deferred in favor of current Dependabot policy unless a future grouped package-manager policy needs Renovate-specific features.

Validation:

- `python -m unittest tests.test_build_release_evidence_ledger tests.test_release_provenance_policy tests.test_check_quality_gate` passed.
- `python scripts\check_release_provenance_policy.py` passed.
- `python scripts\check_quality_gate.py` passed.
- `make quality` passed: Ruff lint/format, ty strict type check, typos, zizmor, taplo, actionlint, quality configuration, release provenance policy, and 45 unit tests.

Deferred:

- `uv sync --frozen` and committed lock-file enforcement remain deferred to the package/CLI migration track because this repository still uses transitional script-based dependency manifests.
