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

## UV Lock And Frozen Sync Enforcement - 2026-06-10

Repo-side hardening applied:

- Added project/dependency metadata to `pyproject.toml` and kept `package = false` while script entrypoints remain transitional.
- Added committed `uv.lock`.
- Added `uv==0.11.8` to the `pyproject.toml` dev dependency group and `uv.lock`, and added an explicit CI bootstrap step so CI can install the uv CLI before lock checks.
- Added `uv-lock` and `uv-sync` Makefile targets.
- Added `uv lock --check` and `uv sync --frozen --all-groups` to `.github/workflows/quality.yml`.
- Updated `scripts/check_quality_gate.py` so quality checks require pinned `uv`, project metadata, committed `uv.lock`, Makefile targets, workflow commands, and documentation.
- Updated `docs/quality-gate.md` to remove the uv deferral and document the enforced frozen sync.

Validation:

- `uv lock --check` passed.
- `uv sync --frozen --all-groups` passed.
- `make quality` passed with uv lock check, frozen sync, Ruff lint/format, ty strict type check, typos, zizmor, taplo, actionlint, quality configuration, release provenance policy, and 45 unit tests.

Operational note:

- On this OneDrive-backed Windows workspace, uv's default user cache hit local permission issues. Validation used `UV_CACHE_DIR=C:\tmp\corpus-nz-hansard-uv-cache`; GitHub-hosted runners should use their normal writable runner cache paths.
