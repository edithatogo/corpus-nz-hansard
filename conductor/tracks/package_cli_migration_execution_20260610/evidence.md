# Evidence: Package And CLI Migration Execution

Status: complete.

Release status: release-ready-package-cli-compatibility-layer.

Implemented artifacts:

- `src/nz_hansard_corpus/__init__.py`
- `src/nz_hansard_corpus/cli.py`
- `scripts/cli.py`
- `manifests/package_cli_migration_execution.json`
- `docs/package-cli-migration-execution.md`
- `scripts/check_package_cli_migration_execution.py`
- `tests/test_package_cli_migration_execution.py`

The legacy scripts remain supported. The publication boundary is preserved because the new CLI dispatch layer only maps commands to existing scripts and this validation does not call live publication operations.

Validated commands include `nzhc build-manifest`, `nzhc validate`, `nzhc metadata build`, `nzhc hf stage`, and `nzhc zenodo draft`.
