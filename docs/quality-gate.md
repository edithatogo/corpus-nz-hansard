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
python scripts/check_corpus_family_engineering_alignment.py
python scripts/check_authority_sources.py
python scripts/check_historical_coverage_audit.py
python scripts/check_release_ladder.py
python scripts/check_gold_evaluation_datasets.py
python scripts/check_canonical_id_uri_policy.py
python scripts/check_dependency_extras_policy.py
python scripts/check_nz_parliamentary_procedure_model.py
python scripts/check_neutral_component_model.py
python scripts/check_akoma_ntoso_endpoint.py
python scripts/check_parlamint_nz_endpoint.py
python scripts/check_popolo_opencivicdata_endpoint.py
python -m unittest discover tests
```

`scripts/check_quality_gate.py` guards the quality configuration itself: dev-tool pins, required Quality workflow commands, local Makefile targets, committed `uv.lock`, packaged `pyproject.toml` metadata with a pinned uv tool dependency, pinned GitHub Actions, and publication workflows staying manual-only.

`scripts/check_release_provenance_policy.py` guards release evidence and provenance wiring: the release evidence ledger schema, Zenodo attestation permissions, pinned attestation action, attested subject paths, documentation coverage, and publication workflows staying manual-only.

`scripts/check_release_version_consistency.py` guards SemVer, DOI, publication URL, citation, release-note, dataset-card, and public-manifest consistency. It also keeps `docs/bleeding-edge-versioning-ci-quality.md` as the documented authority for code/package, dataset, schema, Hugging Face revision, Zenodo DOI snapshot, and manifest-hash governance.

`scripts/check_public_surface_audit.py` guards the public-surface evidence ledger for GitHub, Hugging Face, Zenodo, OSF, and future metadata environments. It keeps active-public claims aligned with `manifests/public_dataset_release_manifest.json` and blocks OSF/future-metadata publication claims until their follow-up tracks land.

`scripts/check_zenodo_rights_metadata.py` guards `.zenodo.json`, the mixed-rights `other-open` Zenodo metadata decision, token naming for any future `zenodraft/action@0.13.3` migration, and the protected-publication boundary.

`scripts/check_shared_core_schema.py`, `scripts/check_metadata_packages.py`, `scripts/check_osf_optional_mirror_policy.py`, `scripts/check_corpus_family_alignment.py`, `scripts/check_corpus_family_engineering_alignment.py`, `scripts/check_authority_sources.py`, `scripts/check_historical_coverage_audit.py`, `scripts/check_release_ladder.py`, `scripts/check_gold_evaluation_datasets.py`, `scripts/check_canonical_id_uri_policy.py`, `scripts/check_dependency_extras_policy.py`, `scripts/check_nz_parliamentary_procedure_model.py`, `scripts/check_neutral_component_model.py`, `scripts/check_akoma_ntoso_endpoint.py`, `scripts/check_parlamint_nz_endpoint.py`, and `scripts/check_popolo_opencivicdata_endpoint.py` guard the shared corpus schema contract, planned metadata package roadmap, OSF inactive-claim boundary, corpus-family publication naming decisions, the package/CLI migration boundary, authority-source discovery coverage, the distinction between supplied DocumentsDB extract coverage and full historical NZ Hansard completeness, the document-level/authority-source/neutral-component/endpoint/upstream-contribution release ladder, reviewed gold/evaluation fixtures for derived fields, stable ID/URI policy for endpoint publication, the optional dependency-group policy in `manifests/dependency_extras_policy.json`, the NZ parliamentary procedure model in `manifests/nz_parliamentary_procedure_model.json`, the neutral component model in `manifests/neutral_component_model.json`, the Akoma Ntoso sample endpoint in `manifests/akoma_ntoso_validation_manifest.json`, the ParlaMint-NZ sample endpoint in `manifests/parlamint_nz_validation_manifest.json`, and the Popolo/Open Civic Data sample endpoint in `manifests/popolo_opencivicdata_validation_manifest.json`. Endpoint validation manifests must record `tool_versions`, `library_versions`, `model_versions`, use `pin-before-release-artifact` for release-affecting stacks, and keep install checks `deferred-until-implementation` until endpoint work begins.

`uv lock --check` and `uv sync --frozen --all-groups` are enforced locally and in CI. The repository is configured as a non-package uv project while script entrypoints remain transitional, so lock-file enforcement can land before the future `src/` package and CLI migration. Pre-commit remains deferred until that package/CLI migration, because CI is the current source of enforcement and avoids adding another local bootstrap path before the dependency model is settled.

Dependency automation currently uses Dependabot for GitHub Actions and pip manifests. Renovate remains deferred unless the repo adopts grouped package-manager policy that Dependabot cannot express.
