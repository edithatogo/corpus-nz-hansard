# Evidence: Corpus Family Engineering Alignment

## Initial Evidence

Status: opened on 2026-06-09.

This track records engineering-alignment requirements between `corpus-nz-hansard` and the legislation sibling using preferred label `corpus-nz-legislation`.

## Current Baseline

Hansard is a strict script-workspace repository with `pyproject.toml`, `uv.lock`,
Ruff, `ty`, `typos`, `zizmor`, `taplo`, `actionlint`, CodeQL, Scorecard, and
protected Zenodo publication boundaries already enforced through `make quality`
and `.github/workflows/quality.yml`.

The legislation sibling at `C:/Users/60217257/OneDrive - Flinders/repos/corpus-law-nz`
was inspected for the engineering baseline. It currently has
`src/nz_legislation_corpus`, `uv.lock`, `pytest`, Ruff, a strict type-checking
target, `.pre-commit-config.yaml`, `renovate.json`, CodeQL, Scorecard, Zenodo
archive workflow automation, and a CLI entry point `nzlc`.

## Migration Target

Added `manifests/corpus_family_engineering_alignment.json` and
`schemas/corpus_family_engineering_alignment.schema.json` to record:

- adopted Hansard standards: `uv.lock`, Ruff, `ty`, CodeQL, Scorecard, and
  protected Zenodo draft/publish boundaries;
- future implementation standards: `src/` package layout, Typer CLI, pytest,
  pre-commit, and Renovate;
- target package `nz_hansard_corpus` and CLI `nzhc`;
- compatibility-wrapper obligations for existing `python scripts/*.py` commands;
- `requirements.txt` / `requirements/dev.txt` transition policy;
- GitHub, Hugging Face, Zenodo, OSF, and future metadata engineering constraints.

Added `docs/corpus-family-engineering-alignment.md` as the human-readable
implementation-ready migration plan.

## CI And Security

Added `scripts/check_corpus_family_engineering_alignment.py` and
`tests/test_corpus_family_engineering_alignment.py`. The checker is wired into
`Makefile`, `.github/workflows/quality.yml`, `docs/quality-gate.md`, and
`scripts/check_quality_gate.py`.

The checker intentionally keeps package layout, Typer CLI, pytest migration,
pre-commit, and Renovate marked as future work. If those files appear before a
package/CLI implementation track updates this ledger, the checker fails so the
planning boundary cannot silently drift.

## Focused Validation

- `python scripts\check_corpus_family_engineering_alignment.py`
- `python -m unittest tests.test_corpus_family_engineering_alignment`
