# Maturity Dependency Checklist — corpus-nz-hansard

> **Context:** Python 3.14 (migrated), pixi + pip, ruff py314, CI on windows-2025-vs2026.

| Category | Status | Rationale |
|---|---|---|
| **Python environment manager (uv/pixi)** | `required` | Active: `pixi.toml` + `pixi.lock` committed, `pixi install` used in all CI workflows. No `uv` — pixi is the single source of truth. |
| **Python lint/format (ruff)** | `required` | Fully configured in `pyproject.toml` with `target-version = "py314"`, `select = ["ALL"]`, explicit ignores. `lint` / `format-check` pixi tasks run in CI quality gate. |
| **Python type checking (ty/pyright)** | `required` | Three type checkers in dev deps (`ty`, `basedpyright`, `pyrefly`). Primary task `typecheck` uses `ty` with `--error all`. Also `typecheck-basedpyright` and `typecheck-pyrefly` tasks. |
| **Python logging (loguru)** | `required` | Core dependency pinned in `pixi.toml`. Enforced via `[tool.legal_nz] logging = "loguru"` convention. |
| **Python CLI UX (typer/rich)** | `optional` | Currently uses `argparse` in `scripts/cli.py` — functional but bare. No typer or rich dependency. Upgrade could improve help output, subcommand ergonomics, and error display. |
| **Config/env loading (pydantic-settings)** | `required` | `pydantic-settings` is a core dependency, used for `.env` / environment-driven configuration. |
| **Boundary validation (pydantic v2)** | `required` | `pydantic` v2 pinned as core dependency. Used for schema validation throughout the codebase. |
| **Hot record serialization (msgspec)** | `optional` | Available as `fast-json` optional feature (`msgspec==0.21.1`, `orjson==3.11.9`). Not in default dependency set — gated for performance-critical pipelines. |
| **Dataframes (polars)** | `required` | Core dependency (`polars>=1.41.2`). Used across scripts for DataFrame-heavy processing. |
| **Query validation (duckdb)** | `required` | Core dependency (`duckdb==1.5.4`). Dedicated `build_duckdb.py` script and manifest validation. |
| **Columnar data (pyarrow/Parquet)** | `required` | Core dependency (`pyarrow==24.0.0`). Parquet is the interchange format for the corpus. |
| **JSON schema (jsonschema)** | `required` | Core dependency (`jsonschema==4.26.0`). 60+ JSON manifest files in `manifests/` validated against schemas in `schemas/`. |
| **HTTP clients (httpx/requests)** | `required` | `requests` is a core dependency. Used for fetching external data (bills API, HathiTrust, Wikipedia, Wikidata, Parliament). |
| **Retry/backoff** | `required` | Repo-local `scripts/http_retry.py` provides bounded exponential backoff for selected acquisition scripts without adding another dependency. Expand this helper as additional flaky-network paths are hardened. |
| **HTML parsing (beautifulsoup4/selectolax)** | `deferred` | No HTML parser in deps. Several scrapers exist but use PDF/structured endpoints. Would be needed if scraping moves beyond structured API calls. |
| **Terminal UI (rich)** | `optional` | Not currently used. CLI is argparse-based with loguru output. `rich` could enhance progress bars and diagnostic display but is not critical. |
| **Checksums/manifests** | `required` | Extensive. 60+ JSON validation manifests in `manifests/`, dedicated `check_*` scripts, schema validation via `jsonschema`. Core to the release pipeline. |
| **Local vector store (lancedb)** | `optional` | Not used. The `search` feature provides `tantivy` (BM25) + `sqlite-vec` (vector) instead. LanceDB could replace this stack but is not needed currently. |
| **Service vector DB (qdrant)** | `not_applicable` | No remote vector DB dependency. All search is local (tantivy + sqlite-vec). This repo publishes data, not serving vectors. |
| **RAG orchestration (haystack)** | `not_applicable` | No RAG framework dependency. The `search` feature provides direct tantivy/sqlite-vec access without orchestration layers. |
| **HF publication (huggingface_hub/datasets)** | `required` | `huggingface-hub` is a core dependency. Dedicated CI workflow (`huggingface_publish.yml`) and test suite (`test_upload_huggingface_dataset.py`, `test_stage_huggingface_dataset.py`). |
| **Archive/DOI (Zenodo/OSF)** | `required` | `.zenodo.json` committed, three Zenodo CI workflows (`zenodo_archive.yml`, `zenodo_metadata.yml`, `zenodo_publish.yml`). OSF mirror policy manifest at `manifests/osf_optional_mirror_policy.json` with dedicated checker script. |
