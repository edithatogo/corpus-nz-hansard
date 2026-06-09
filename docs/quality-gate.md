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
python scripts/check_release_version_consistency.py
python scripts/check_public_surface_audit.py
python scripts/check_zenodo_rights_metadata.py
python scripts/check_shared_core_schema.py
python scripts/check_metadata_packages.py
python scripts/check_osf_optional_mirror_policy.py
python scripts/check_corpus_family_alignment.py
python -m unittest discover tests
```

`scripts/check_quality_gate.py` guards the quality configuration itself: dev-tool pins, required Quality workflow commands, local Makefile targets, committed `uv.lock`, packaged `pyproject.toml` metadata with a pinned uv tool dependency, pinned GitHub Actions, and publication workflows staying manual-only.

`scripts/check_release_provenance_policy.py` guards release evidence and provenance wiring: the release evidence ledger schema, Zenodo attestation permissions, pinned attestation action, attested subject paths, documentation coverage, and publication workflows staying manual-only.

`scripts/check_release_version_consistency.py` guards SemVer, DOI, publication URL, citation, release-note, dataset-card, and public-manifest consistency. It also keeps `docs/bleeding-edge-versioning-ci-quality.md` as the documented authority for code/package, dataset, schema, Hugging Face revision, Zenodo DOI snapshot, and manifest-hash governance.

`scripts/check_public_surface_audit.py` guards the public-surface evidence ledger for GitHub, Hugging Face, Zenodo, OSF, and future metadata environments. It keeps active-public claims aligned with `manifests/public_dataset_release_manifest.json` and blocks OSF/future-metadata publication claims until their follow-up tracks land.

`scripts/check_zenodo_rights_metadata.py` guards `.zenodo.json`, the mixed-rights `other-open` Zenodo metadata decision, token naming for any future `zenodraft/action@0.13.3` migration, and the protected-publication boundary.

`scripts/check_shared_core_schema.py`, `scripts/check_metadata_packages.py`, `scripts/check_osf_optional_mirror_policy.py`, and `scripts/check_corpus_family_alignment.py` guard the shared corpus schema contract, planned metadata package roadmap, OSF inactive-claim boundary, and corpus-family publication naming decisions.

`uv lock --check` and `uv sync --frozen --all-groups` are enforced locally and in CI. The repository is configured as a non-package uv project while script entrypoints remain transitional, so lock-file enforcement can land before the future `src/` package and CLI migration. Pre-commit remains deferred until that package/CLI migration, because CI is the current source of enforcement and avoids adding another local bootstrap path before the dependency model is settled.

Dependency automation currently uses Dependabot for GitHub Actions and pip manifests. Renovate remains deferred unless the repo adopts grouped package-manager policy that Dependabot cannot express.
