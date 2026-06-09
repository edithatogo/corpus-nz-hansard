# Technical Context

## Current State

This workspace currently contains a single ZIP archive of CSV extracts and no application, package, or pipeline metadata.

## Known Data Shape

Archive listing:

- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-47.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-48.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-49.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-50.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-51.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-52.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-53.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-54.csv`

## Preferred Tooling

Use conservative, scriptable tools that work well on Windows and large CSV files:

- PowerShell for local file inventory and orchestration.
- Python for archive inspection, CSV schema discovery, normalization, validation, and manifest generation.
- SQLite or DuckDB for local exploratory indexing once CSV schemas are known.
- Parquet for columnar derived outputs if publication or repeated analysis requires it.

## Interoperability Tooling

Preferred libraries for endpoint implementation:

- `pandas`, `pyarrow`, and `duckdb` for the current neutral tabular pipeline.
- `polars` for larger derived transforms when performance pressure justifies another dependency.
- `jsonschema`, `pydantic`, and `pandera` for schema and tabular validation.
- `lxml` and `xmlschema` for TEI/ParlaMint and Akoma Ntoso XML generation; use external `jing` when Relax NG validation is required.
- `rdflib`, `pyshacl`, and `linkml` for RDF, SHACL, and linked-data schema work.
- `rapidfuzz` for authority-source name matching.
- `spacy`, `stanza`, `conllu`, and `pyconll` for NLP, Universal Dependencies, and CoNLL-U exports.
- `transformers`, `sentence-transformers`, and `scikit-learn` for topic classifiers, embeddings, and model-backed review workflows.
- `bertopic` only for exploratory topic modelling unless a later validation track promotes a topic model to a governed artifact.
- `frictionless`, `rocrate`, and `mlcroissant` for Frictionless Data Package, RO-Crate, and Croissant metadata.

Authority-source validation remains required for members, parties, votes, and official parliamentary structure. Generic NLP output is not enough for authoritative derived fields.

Keep `requirements.txt` as the base runtime. Add heavy XML, RDF, NLP, ML, and metadata libraries through grouped requirements or package extras when the relevant endpoint track begins.

## Repository Constraints

- The Git repository root appears to be higher than this project directory, so status output may include unrelated OneDrive-wide changes.
- Keep all generated project files scoped under `corpus-nz-hansard`.
- Avoid extracting multi-gigabyte data into the repository root without an explicit track and output policy.

## Data Handling

- Treat the ZIP as the immutable source artifact.
- Prefer derived-output directories that can be ignored or regenerated.
- Record source file hashes and row counts before transformation.
- Validate CSV dialect, encoding, headers, null handling, and date fields before building downstream models.

## Power BI Note

The local AGENTS instructions include Power BI CLI skill requirements for Power BI, DAX, semantic model, and report-layer work. This setup did not perform Power BI work. Invoke the relevant Power BI skill before future Power BI-specific changes.

## Publication and metadata environments

Track publication alignment across:

- GitHub for code, CI, releases, security posture, repository metadata, and lightweight artifacts.
- Hugging Face Datasets for operational/canonical Parquet publication, dataset cards, Xet-backed storage, access/gating state, and viewer health.
- Zenodo for immutable DOI snapshots, archive manifests, checksums, related identifiers, and source-rights-safe license metadata.
- OSF as an optional review or mirror environment only after a policy exists.
- Generated metadata packages such as Croissant, RO-Crate, Frictionless Data Package, DCAT, and PROV-O as future SOTA discovery/interoperability surfaces.


## Zenodraft requirement

Future Zenodo draft/archive workflow changes should use or formally evaluate https://github.com/zenodraft/zenodraft. Use sandbox first, validate .zenodo.json metadata, map tokens to ZENODO_ACCESS_TOKEN or ZENODO_SANDBOX_ACCESS_TOKEN only inside the relevant CI step, and keep publish commands behind protected reviewer approval.


## Bleeding-edge automation target

The corpus-family target is documented in `docs/bleeding-edge-versioning-ci-quality.md`. Prefer Rust-backed tooling where practical: `uv` for Python dependency management, `ruff` for lint/format/imports, `typos` for spelling/identifier checks, `zizmor` for GitHub Actions security linting, `taplo` for TOML linting, and local `ripgrep` for maintenance audits. Retain best-in-class non-Rust tools where needed, including `mypy` or `pyright`, CodeQL, OpenSSF Scorecard, Renovate, and `actionlint`.

Release automation should separate code/package versions, dataset versions, schema versions, Hugging Face revisions, Zenodo DOI snapshots, and manifest hashes. Zenodo draft workflows should use or formally evaluate `https://github.com/zenodraft/zenodraft`.

## Transitional packaging note

`requirements.txt` remains the current runtime input until the engineering-alignment track migrates Hansard to `pyproject.toml`, `uv.lock`, `src/nz_hansard_corpus`, a Typer CLI, pytest, ruff, mypy/pyright, pre-commit, Renovate, CodeQL, Scorecard, and Rust-backed quality tooling. Treat `requirements.txt` as transitional, not the long-term standard.
