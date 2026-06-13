# Evidence: Package And CLI Migration Execution

Status: blocked.

Tracked artifacts:

- `spec.md`
- `plan.md`
- `metadata.json`
- `index.md`

Dependency boundary:

- `pyproject.toml` still sets `tool.uv.package = false`.
- `docs/corpus-family-engineering-alignment.md` documents `nz_hansard_corpus`
  and `nzhc` as future migration targets rather than current behavior.
- `scripts/check_corpus_family_engineering_alignment.py` deliberately fails if
  `src/`, `.pre-commit-config.yaml`, or `renovate.json` appear before the
  planning track is updated to implementation mode.
- `docs/quality-gate.md` still describes the repo as a non-package uv project
  with transitional script entrypoints.

What this track would add later:

- a `src/nz_hansard_corpus` package layout
- a Typer-style `nzhc` CLI
- backwards-compatible wrappers for current `python scripts/*.py` entrypoints
- transition documentation for the old and new invocation paths

Current blocker:

- The migration boundary is intentionally not active yet, and the repo’s
  current quality gate treats package layout, Typer CLI, pytest migration,
  pre-commit, and Renovate as future work.

Reference surfaces:

- `docs/corpus-family-engineering-alignment.md`
- `conductor/tracks/corpus_family_engineering_alignment_20260609/evidence.md`
- `docs/quality-gate.md`
- `scripts/check_corpus_family_engineering_alignment.py`
