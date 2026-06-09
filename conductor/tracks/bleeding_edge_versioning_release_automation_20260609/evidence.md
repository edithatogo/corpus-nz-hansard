# Evidence: Bleeding Edge Versioning And Release Automation

## Initial Evidence

Status: opened on 2026-06-09.

This track implements the corpus-family bleeding-edge versioning, CI/CD, code-quality, automation, and provenance standard.

## Version Governance And Consistency Gate - 2026-06-10

Status: complete.

Implemented:

- Added `docs/bleeding-edge-versioning-ci-quality.md` as the release-governance authority for:
  - current and target state;
  - code/package version authority;
  - dataset version authority;
  - schema version authority;
  - Hugging Face revision authority;
  - Zenodo DOI snapshot authority;
  - manifest hash authority;
  - Release Please decision;
  - publication safety gates.
- Deferred Release Please for the already-published `0.1.0` artifact and recorded the current equivalent policy: Conventional Commit messages, manual publication workflows only, version-consistency checks, and provenance-policy checks.
- Added `scripts/check_release_version_consistency.py` to enforce consistency across `VERSION`, `pyproject.toml`, `CITATION.cff`, `RELEASE_NOTES.md`, `DATASET_CARD.md`, and `manifests/public_dataset_release_manifest.json`.
- Added `tests/test_check_release_version_consistency.py`.
- Added `version-consistency` to `Makefile`.
- Added `Release version consistency` to `.github/workflows/quality.yml` with read-only repository permissions inherited from the Quality workflow.
- Updated `docs/quality-gate.md` and `scripts/check_quality_gate.py` so the new check is part of the documented and enforced quality gate.

Current authoritative values enforced by the checker:

- Version: `0.1.0`.
- GitHub repository: `https://github.com/edithatogo/corpus-nz-hansard`.
- GitHub release: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0`.
- Hugging Face dataset: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`.
- Zenodo DOI: `10.5281/zenodo.20595194`.
- Zenodo record: `https://zenodo.org/records/20595194`.

Verification:

- Red phase: `python -m unittest tests.test_check_release_version_consistency` failed before `scripts/check_release_version_consistency.py` existed.
- `python -m unittest tests.test_check_release_version_consistency` passed.
- `python -m unittest tests.test_check_quality_gate` passed.
- `python scripts\check_release_version_consistency.py` passed.
- `make quality` passed after Ruff formatting, including uv lock check, frozen sync, Ruff, ty, typos, zizmor, taplo, actionlint, quality configuration, release provenance policy, release version consistency, and 46 unit tests.
