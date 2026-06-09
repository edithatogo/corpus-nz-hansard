# Evidence: Dependency Extras Policy

- Initial dependency policy is documented in `docs/dependency-policy.md`.
- Optional requirement groups are listed under `requirements/`.
- Base runtime dependency floor updates were merged/applied after green Dependabot checks on 2026-06-09: `jsonschema>=4.26.0`, `requests>=2.34.2`, `huggingface_hub>=1.18.0`, and `polars>=1.41.2`.
- Local test infrastructure now supports `CORPUS_NZ_HANSARD_TEST_TMP` and falls back from a locked fixed temp directory to a unique run directory.
- Remaining hardening: migrate to a lockfile or generated constraints file before endpoint stacks become part of release CI.
