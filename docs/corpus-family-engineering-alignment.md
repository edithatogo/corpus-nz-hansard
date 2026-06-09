# Corpus Family Engineering Alignment

This document records how `corpus-nz-hansard` should align with the
`corpus-nz-legislation` engineering baseline without weakening the current
Hansard release evidence.

## Current Baseline

Hansard is currently a strict script-workspace repository. The local and CI
quality baseline is `make quality`, including `uv lock --check`,
`uv sync --frozen --all-groups`, Ruff lint and format, `ty`, `typos`, `zizmor`,
`taplo`, `actionlint`, policy checkers, and `unittest` discovery.

The legislation sibling currently uses a package-first baseline:

- `src/nz_legislation_corpus`
- `uv.lock`
- `pytest`
- Ruff
- strict type checking target
- `.pre-commit-config.yaml`
- `renovate.json`
- CodeQL
- OpenSSF Scorecard
- a CLI entry point named `nzlc`

Hansard already has `pyproject.toml`, `uv.lock`, Ruff, `ty`, CodeQL, Scorecard,
and protected Zenodo publication boundaries. Hansard does not yet have a
`src/` package layout, Typer CLI, pytest migration, pre-commit config, or
Renovate config.

## Migration Target

The future package name is `nz_hansard_corpus`; the future CLI is `nzhc`.
This track does not perform that refactor. It records the compatibility gates
that a future package/CLI track must satisfy.

Existing `python scripts/*.py` commands remain supported until all of the
following are true:

- replacement CLI commands exist;
- wrapper parity tests cover the old and new invocation paths;
- release documentation lists the old command, replacement command, and
  deprecation window;
- CI runs both old wrappers and new CLI paths for at least one transition
  release;
- publication jobs remain manually dispatched and protected.

`requirements.txt` and `requirements/dev.txt` remain supported during the
transition. Dependency authority can move fully to `pyproject.toml` and
`uv.lock` only after documentation, CI, and wrappers agree.

## Target Commands

| Future command | Compatibility obligation |
| --- | --- |
| `nzhc build-manifest` | Preserve current manifest and public-surface builder outputs. |
| `nzhc validate` | Preserve policy checker behavior and `make quality` coverage. |
| `nzhc metadata build` | Preserve `scripts/build_metadata_packages.py` outputs and checksums. |
| `nzhc hf stage` | Preserve Hugging Face viewer layout and asset placement. |
| `nzhc zenodo draft` | Preserve draft/update-only behavior and protected production publish boundary. |

## CI And Security

Ubuntu primary CI can be adopted only after Windows compatibility remains
covered for local OneDrive/PowerShell usage and existing generated evidence.
CodeQL, Scorecard, `zizmor`, `actionlint`, and protected Zenodo workflows remain
separate from dependency-update automation.

Renovate and pre-commit are future adoptions. Neither may trigger Hugging Face,
Zenodo, OSF, or future metadata publication jobs.

## Publication Boundaries

GitHub, Hugging Face, Zenodo, OSF, and future metadata environments must be
considered before engineering changes remove scripts or change output paths.
Package migration must preserve active release URLs, generated metadata package
checksums, Hugging Face viewer layout, Zenodo draft-first behavior, and OSF's
inactive optional-mirror status.

Validation:

```powershell
python scripts\check_corpus_family_engineering_alignment.py
python -m unittest tests.test_corpus_family_engineering_alignment
```
