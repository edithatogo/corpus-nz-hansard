# Quality Gate

The current local quality gate mirrors the enforced CI checks while this repository remains in its transitional script-based layout.

Run the full local gate with:

```powershell
make quality
```

Equivalent commands:

```powershell
iwr -UseBasicParsing https://pixi.sh/install.ps1 | iex
pixi install
pixi run lint
pixi run format-check
pixi run typecheck
pixi run typecheck-basedpyright
pixi run typecheck-pyrefly
pixi run spell
pixi run workflow-audit
pixi run toml-check
actionlint -color
pixi run python scripts/check_quality_gate.py
pixi run python scripts/check_release_provenance_policy.py
pixi run python scripts/check_release_version_consistency.py
pixi run python scripts/check_public_surface_audit.py
pixi run python scripts/check_zenodo_rights_metadata.py
pixi run python scripts/check_shared_core_schema.py
pixi run python scripts/check_metadata_packages.py
pixi run python scripts/check_osf_optional_mirror_policy.py
pixi run python scripts/check_multi_git_archive_mirroring.py
pixi run python scripts/check_corpus_family_alignment.py
pixi run python scripts/check_corpus_family_engineering_alignment.py
pixi run python scripts/check_authority_sources.py
pixi run python scripts/check_historical_sitting_inventory.py
pixi run python scripts/check_historical_sitting_official_exports.py
pixi run python scripts/build_historical_sitting_official_exports_coverage.py
pixi run python scripts/check_historical_sitting_reconciliation.py
pixi run python scripts/check_historical_coverage_audit.py
pixi run python scripts/check_release_ladder.py
pixi run python scripts/check_gold_evaluation_datasets.py
pixi run python scripts/check_canonical_id_uri_policy.py
pixi run python scripts/check_dependency_extras_policy.py
pixi run python scripts/check_nz_parliamentary_procedure_model.py
pixi run python scripts/check_neutral_component_model.py
pixi run python scripts/check_akoma_ntoso_endpoint.py
pixi run python scripts/check_parlamint_nz_endpoint.py
pixi run python scripts/check_popolo_opencivicdata_endpoint.py
pixi run python scripts/check_ud_conllu_endpoint.py
pixi run python scripts/check_rdf_linked_data_endpoint.py
pixi run python scripts/validate_derived_fields.py
pixi run test
pixi run test-offline
pixi run benchmark
pixi run security-audit
pixi run dependency-check
pixi run dead-code
```

`scripts/check_quality_gate.py` guards the quality configuration itself: dev-tool pins, required Quality workflow commands, local Makefile targets, committed `pixi.toml`, Python 3.14 package metadata, pinned Pixi PyPI dependencies, pinned GitHub Actions, and publication workflows staying manual-only.

`scripts/check_release_provenance_policy.py` guards release evidence and provenance wiring: the release evidence ledger schema, Zenodo attestation permissions, pinned attestation action, attested subject paths, documentation coverage, and publication workflows staying manual-only.

`scripts/check_release_version_consistency.py` guards SemVer, DOI, publication URL, citation, release-note, dataset-card, and public-manifest consistency. It also keeps `docs/bleeding-edge-versioning-ci-quality.md` as the documented authority for code/package, dataset, schema, Hugging Face revision, Zenodo DOI snapshot, and manifest-hash governance.

`scripts/check_public_surface_audit.py` guards the public-surface evidence ledger for GitHub, Hugging Face, Zenodo, OSF, and future metadata environments. It keeps active-public claims aligned with `manifests/public_dataset_release_manifest.json` and blocks OSF/future-metadata publication claims until their follow-up tracks land.

`scripts/check_zenodo_rights_metadata.py` guards `.zenodo.json`, the mixed-rights `other-open` Zenodo metadata decision, token naming for any future `zenodraft/action@0.13.3` migration, and the protected-publication boundary.

`scripts/check_shared_core_schema.py`, `scripts/check_metadata_packages.py`, `scripts/check_osf_optional_mirror_policy.py`, `scripts/check_multi_git_archive_mirroring.py`, `scripts/check_corpus_family_alignment.py`, `scripts/check_corpus_family_engineering_alignment.py`, `scripts/check_authority_sources.py`, `scripts/check_historical_sitting_inventory.py`, `scripts/check_historical_sitting_official_exports.py`, `scripts/build_historical_sitting_official_exports_coverage.py`, `scripts/check_historical_sitting_reconciliation.py`, `scripts/check_historical_coverage_audit.py`, `scripts/check_release_ladder.py`, `scripts/check_gold_evaluation_datasets.py`, `scripts/check_canonical_id_uri_policy.py`, `scripts/check_dependency_extras_policy.py`, `scripts/check_nz_parliamentary_procedure_model.py`, `scripts/check_neutral_component_model.py`, `scripts/check_akoma_ntoso_endpoint.py`, `scripts/check_parlamint_nz_endpoint.py`, `scripts/check_popolo_opencivicdata_endpoint.py`, `scripts/check_ud_conllu_endpoint.py`, `scripts/check_rdf_linked_data_endpoint.py`, and `scripts/validate_derived_fields.py` guard the shared corpus schema contract, planned metadata package roadmap, OSF inactive-claim boundary, the multi-git mirror workflow triggers, pinned checkout, required secrets, dry-run/secret-pair skip behavior, and OSF policy linkage, corpus-family publication naming decisions, the package/CLI migration boundary, authority-source discovery coverage, the official sitting inventory used for reconciliation, the official PDF export path used to avoid the HTML challenge layer, the date-level comparison probe against the corpus ledger, the historical sitting reconciliation contract, the distinction between supplied DocumentsDB extract coverage and full historical NZ Hansard completeness, the document-level/authority-source/neutral-component/endpoint/upstream-contribution release ladder, reviewed gold/evaluation fixtures for derived fields, stable ID/URI policy for endpoint publication, the optional dependency-group policy in `manifests/dependency_extras_policy.json`, the NZ parliamentary procedure model in `manifests/nz_parliamentary_procedure_model.json`, the neutral component model in `manifests/neutral_component_model.json`, the Akoma Ntoso sample endpoint in `manifests/akoma_ntoso_validation_manifest.json`, the ParlaMint-NZ sample endpoint in `manifests/parlamint_nz_validation_manifest.json`, the Popolo/Open Civic Data sample endpoint in `manifests/popolo_opencivicdata_validation_manifest.json`, the Universal Dependencies / CoNLL-U sample endpoint in `manifests/ud_conllu_validation_manifest.json`, the RDF / Linked Data sample endpoint in `manifests/rdf_linked_data_validation_manifest.json`, and the derived-fields validation manifests in `manifests/member_identity_resolution_validation.json`, `manifests/party_attribution_validation.json`, and `manifests/speech_turn_validated_artifact_validation.json`. Endpoint validation manifests must record `tool_versions`, `library_versions`, `model_versions`, use `pin-before-release-artifact` for release-affecting stacks, and keep install checks `deferred-until-implementation` until endpoint work begins.

`pixi install` is enforced locally and in CI. The repository now uses Pixi as the environment manager while script entrypoints remain transitional, so the environment contract can land before the future `src/` package and CLI migration. Pre-commit remains deferred until that package/CLI migration, because CI is the current source of enforcement and avoids adding another local bootstrap path before the dependency model is settled.

Additional explicit quality lanes are available for stricter review and release preparation:

```powershell
pixi run typecheck-basedpyright
pixi run typecheck-pyrefly
pixi run test-offline
pixi run benchmark
pixi run profile-search-index
pixi run security-audit
pixi run sbom
pixi run dependency-check
pixi run dead-code
pixi run mutation-smoke
```

The Pixi `all` environment includes lightweight quality, AI-agent, JSON, XML-model, query, and search tooling. The `embeddings` environment is intentionally separate because it can install multi-gigabyte model/runtime wheels such as PyTorch; endpoint tracks must opt into it explicitly and record model/runtime evidence before producing release-affecting artifacts.

Dependency automation currently uses Dependabot for GitHub Actions and pip manifests. Renovate remains deferred unless the repo adopts grouped package-manager policy that Dependabot cannot express.
