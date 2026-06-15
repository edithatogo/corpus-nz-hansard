# CLI-first entrypoints

Use `corpus-nz-hansard` before invoking repository scripts directly.

## Commands

- `corpus-nz-hansard --list` lists approved aliases.
- `corpus-nz-hansard <alias> -- <script-args>` dispatches to the existing script implementation.

## Approved aliases

- `duckdb` -> `scripts/build_duckdb.py`
- `hf-stage` -> `scripts/stage_huggingface_dataset.py`
- `hf-upload` -> `scripts/upload_huggingface_dataset.py`
- `inventory` -> `scripts/inventory_archive.py`
- `normalize` -> `scripts/normalize_hansard.py`
- `quality-gate` -> `scripts/check_quality_gate.py`
- `release-package` -> `scripts/build_release_package.py`
- `schema` -> `scripts/discover_schema.py`
- `search-index` -> `scripts/build_search_index.py`
- `validate-records` -> `scripts/validate_hansard_records.py`
- `zenodo-build` -> `scripts/build_zenodo_archive.py`
- `zenodo-upload` -> `scripts/upload_zenodo_archive.py`

## Policy

Existing `scripts/*.py` files remain implementation modules. New automation, conductor tracks, and swarm prompts should call the package CLI first, then add a new alias here when a repeated workflow is needed.
