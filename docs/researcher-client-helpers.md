# Researcher Client Helpers

## Scope

These helpers are read-only examples for consuming corpus artifacts in local analysis
workflows. They are separate from canonical generation scripts and do not modify source
or release outputs.

## Supported Artifacts

- `samples/researcher-client-helpers/hansard-mini.csv`
- `samples/rdf-linked-data/linked-data.ttl`

The document sample is a tiny local-review fixture. The RDF sample is a maintainer-review
sample package, not a public endpoint release.

## Python helper

Use Python when you want a quick inspection of the document-level sample:

```python
from pathlib import Path
from scripts.researcher_client_helpers import python_document_summary

summary = python_document_summary(Path("samples/researcher-client-helpers/hansard-mini.csv"))
print(summary["row_count"])
print(summary["document_types"])
```

## DuckDB helper

Use DuckDB when you want grouped counts from the same sample:

```python
from pathlib import Path
from scripts.researcher_client_helpers import duckdb_document_summary

summary = duckdb_document_summary(Path("samples/researcher-client-helpers/hansard-mini.csv"))
print(summary["rows_by_document_type"])
```

The same helper also accepts a generated Parquet path later, for example
`generated/parquet/hansard.parquet`, when that artifact is present in the workspace.

## RDF sample helper

The RDF sample can be inspected with Python and rdflib:

```python
from pathlib import Path
from scripts.researcher_client_helpers import rdf_sample_summary

summary = rdf_sample_summary(Path("samples/rdf-linked-data/linked-data.ttl"))
print(summary["dataset_titles"])
```

## Deferred Helpers

R and standalone SPARQL examples are deferred until RDF endpoint release artifacts are
ready. This keeps the helper surface aligned with the current local-review boundary.

## Validation

- `python scripts/build_researcher_client_helpers.py`
- `python scripts/check_researcher_client_helpers.py`
- `python -m unittest tests.test_researcher_client_helpers`
