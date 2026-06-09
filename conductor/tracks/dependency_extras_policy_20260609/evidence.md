# Evidence: Dependency Extras Policy

- Initial dependency policy is documented in `docs/dependency-policy.md`.
- Optional requirement groups are listed under `requirements/`.
- Base runtime dependency floor updates were merged/applied after green Dependabot checks on 2026-06-09: `jsonschema>=4.26.0`, `requests>=2.34.2`, `huggingface_hub>=1.18.0`, and `polars>=1.41.2`.
- Local test infrastructure now supports `CORPUS_NZ_HANSARD_TEST_TMP` and falls back from a locked fixed temp directory to a unique run directory.

## Dependency Extras Manifest

- Added `manifests/dependency_extras_policy.json` and `schemas/dependency_extras_policy.schema.json`.
- The manifest keeps `requirements.txt` as the base runtime and records governed optional groups for `requirements/data.txt`, `requirements/schema.txt`, `requirements/xml.txt`, `requirements/rdf.txt`, `requirements/authority.txt`, `requirements/nlp.txt`, `requirements/ml.txt`, and `requirements/metadata.txt`.
- Heavy XML, RDF, NLP, ML, metadata, schema, and authority stacks are prohibited from the default runtime unless a later production import requires a scoped policy update.

## Endpoint Validation Requirements

- Endpoint tracks must cite `manifests/dependency_extras_policy.json`.
- Endpoint validation manifests must record `dependency_groups`, `install_commands`, `tool_versions`, `library_versions`, `model_versions`, `lock_or_constraints`, `release_affecting_dependencies`, and `validation_command`.
- Optional install checks remain `deferred-until-implementation` until endpoint implementation begins.
- Release-affecting endpoint stacks use `pin-before-release-artifact`; broad optional planning files are acceptable only before public endpoint artifacts are generated.

## Focused Validation

- Added `scripts/check_dependency_extras_policy.py`.
- Added `tests/test_dependency_extras_policy.py`.
- Wired the dependency extras checker into `make quality`, `.github/workflows/quality.yml`, `docs/quality-gate.md`, and `scripts/check_quality_gate.py`.
