# Package And CLI Migration Execution

Release status: release-ready-package-cli-compatibility-layer.

The package/CLI migration is implemented as a compatibility layer. The repository now exposes the `nz_hansard_corpus` package namespace and the `nzhc` command surface while legacy scripts remain supported.

Implemented command surface:

- `nzhc build-manifest`
- `nzhc validate`
- `nzhc metadata build`
- `nzhc hf stage`
- `nzhc zenodo draft`

The legacy scripts remain supported through `python scripts/*.py` and the existing compatibility console names route through `nz_hansard_corpus.cli:main`. The publication boundary is preserved: this track only wires command dispatch and validation, and does not run live Hugging Face, Zenodo, OSF, or other publication mutations.

Validation:

- `python -m nz_hansard_corpus.cli --list`
- `python scripts/check_package_cli_migration_execution.py`
- `python -m pytest tests/test_package_cli_migration_execution.py`
