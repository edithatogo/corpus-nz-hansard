# Evidence: Zenodo Rights Metadata And Zenodraft Workflow

## Initial Evidence

Status: opened on 2026-06-09.

Evidence should capture current and target public-surface behaviour across GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.

## Protected Publication Boundary - 2026-06-09

Repo-side workflow hardening separates Zenodo draft/update operations from final publication:

- `.github/workflows/zenodo_archive.yml` can build and upload archive files to a draft, but no longer exposes a `publish` input or passes `--publish`.
- `.github/workflows/zenodo_metadata.yml` updates metadata without exposing a publish input.
- `scripts/upload_zenodo_archive.py` creates/updates draft files and metadata without publishing.
- `scripts/update_zenodo_metadata.py` updates metadata without publishing.
- `scripts/publish_zenodo_deposition.py` is the only script that calls the Zenodo publish action.
- `.github/workflows/zenodo_publish.yml` runs that publish script through the `zenodo-production-publish` environment.

Remaining operator requirement: configure `zenodo-production-publish` in GitHub repository settings with required reviewers before using it as a production release approval gate.

## Rights Metadata And Zenodraft Evaluation - 2026-06-10

Status: repo-side implementation complete; sandbox proof blocked by missing `ZENODO_SANDBOX_TOKEN` and side-effect approval.

Repo-side implementation:

- Added `.zenodo.json` for the canonical `0.1.0` release metadata.
- Added `scripts/build_zenodo_metadata.py` to regenerate `.zenodo.json`.
- Added `scripts/check_zenodo_rights_metadata.py` to enforce rights metadata, related identifiers, `other-open` scope, `zenodraft/action@0.13.3` policy, token mapping, and protected publication boundaries.
- Added `tests/test_zenodo_rights_metadata.py`.
- Added `docs/zenodo-rights-and-zenodraft.md`.
- Updated `docs/ZENODO_SETUP.md` with `zenodraft/action@0.13.3`, `.zenodo.json`, `ZENODO_SANDBOX_ACCESS_TOKEN`, `ZENODO_ACCESS_TOKEN`, sandbox-first migration, and `publish: false` requirements.
- Added `zenodo-rights` to `Makefile`, `.github/workflows/quality.yml`, `docs/quality-gate.md`, and `scripts/check_quality_gate.py`.

Rights decision:

- The Zenodo license field remains `other-open`.
- Reason: the archive is a mixed-rights bundle containing MIT-licensed repository materials, derived normalized Parquet, documentation, schemas, manifests, release evidence, and underlying New Zealand Parliamentary Debates/Hansard source text provenance notes. A narrower MIT-only license would overstate the rights scope.
- The controlling scope note is in `.zenodo.json`, `NOTICE.md`, and `docs/licensing-and-provenance.md`: source ZIP not redistributed; source text provenance recorded; repository code/docs/manifests/release tooling MIT licensed; no official New Zealand Parliament endorsement.

Zenodraft evaluation:

- Evaluated source: `https://github.com/zenodraft/action` / Marketplace `zenodraft/action@0.13.3`.
- Relevant documented behavior: metadata file is `.zenodo.json`; `sandbox: true` targets Zenodo Sandbox; `publish` defaults false and must remain `publish: false` for draft/update jobs; action token names are `ZENODO_ACCESS_TOKEN` and `ZENODO_SANDBOX_ACCESS_TOKEN`.
- Adoption decision: defer migration from the existing tested Python REST scripts until `ZENODO_SANDBOX_TOKEN` exists and a maintainer explicitly requests migration.
- Current local runtime exceeds the candidate requirement: Node `v24.15.0`, npm `11.12.1`.
- Existing `ZENODO_TOKEN` / `ZENODO_SANDBOX_TOKEN` should only be mapped to zenodraft-specific environment variables inside the relevant CI step.

Current read-only Zenodo API evidence for `https://zenodo.org/api/records/20595194`:

- `id=20595194`.
- DOI `10.5281/zenodo.20595194`.
- Concept DOI `10.5281/zenodo.20591996`.
- `state=done`.
- `submitted=true`.
- Title `NZ Hansard Corpus`.
- Version `0.1.0`.
- License `other-open`.
- Creator `Dylan Mordaunt`.
- Related identifiers include GitHub repository, GitHub release, and Hugging Face dataset.
- Files: `nz-hansard-corpus-0.1.0.manifest.json` and `nz-hansard-corpus-0.1.0.tar.gz`.

Blocked sandbox proof:

- Sandbox draft/version creation, file upload, metadata update, and prereserved DOI/details readback were not run because no `ZENODO_SANDBOX_TOKEN` is configured in this local session and those commands create external sandbox state.
- Production publication remains isolated in `zenodo_publish.yml` through the `zenodo-production-publish` GitHub environment.

Validation:

- Red phase: `python -m unittest tests.test_zenodo_rights_metadata` failed before `scripts/build_zenodo_metadata.py` existed.
- `python -m unittest tests.test_zenodo_rights_metadata tests.test_check_quality_gate` passed.
- `python scripts\check_zenodo_rights_metadata.py` passed.
- `make quality` passed with uv lock check, frozen sync, Ruff, Ruff format, ty strict type check, typos, zizmor, taplo, actionlint, quality configuration, release provenance policy, release version consistency, public-surface audit, Zenodo rights metadata, and 50 unit tests.
