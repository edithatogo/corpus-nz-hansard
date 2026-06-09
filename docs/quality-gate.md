# Quality Gate

The current local quality gate mirrors the enforced CI checks while this repository remains in its transitional script-based layout.

Run the full local gate with:

```powershell
make quality
```

Equivalent commands:

```powershell
python -m pip install uv==0.11.8
uv lock --check
uv sync --frozen --all-groups
python -m ruff check --no-cache .
python -m ruff format --check --no-cache .
ty check --error all .
typos --config typos.toml
zizmor --min-severity medium .github/workflows
taplo format --check pyproject.toml typos.toml
actionlint -color
python scripts/check_quality_gate.py
python scripts/check_release_provenance_policy.py
python -m unittest discover tests
```

`scripts/check_quality_gate.py` guards the quality configuration itself: dev-tool pins, required Quality workflow commands, local Makefile targets, committed `uv.lock`, packaged `pyproject.toml` metadata with a pinned uv tool dependency, pinned GitHub Actions, and publication workflows staying manual-only.

`scripts/check_release_provenance_policy.py` guards release evidence and provenance wiring: the release evidence ledger schema, Zenodo attestation permissions, pinned attestation action, attested subject paths, documentation coverage, and publication workflows staying manual-only.

`uv lock --check` and `uv sync --frozen --all-groups` are enforced locally and in CI. The repository is configured as a non-package uv project while script entrypoints remain transitional, so lock-file enforcement can land before the future `src/` package and CLI migration. Pre-commit remains deferred until that package/CLI migration, because CI is the current source of enforcement and avoids adding another local bootstrap path before the dependency model is settled.

Dependency automation currently uses Dependabot for GitHub Actions and pip manifests. Renovate remains deferred unless the repo adopts grouped package-manager policy that Dependabot cannot express.
