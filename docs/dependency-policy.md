# Dependency Policy

## Purpose

Keep the base corpus pipeline reproducible and lightweight while allowing endpoint-specific toolchains for XML, RDF, NLP, ML, and metadata work.

## Current Base Runtime

The current `requirements.txt` is the base runtime:

| Dependency | Purpose |
| --- | --- |
| `duckdb==1.5.3` | Local analytical database generation and validation. |
| `pyarrow` | Parquet and Arrow table generation. |
| `polars>=1.41.2` | Dataframe transforms and larger derived-table workflows. |
| `jsonschema>=4.26.0` | JSON Schema validation. |
| `requests>=2.34.2` | Zenodo and metadata API calls. |
| `huggingface_hub>=1.18.0` | Hugging Face dataset publication. |

## Optional Dependency Groups

Endpoint work should add grouped requirements or package extras rather than expanding the base runtime by default.

| Group | Dependencies | Use |
| --- | --- | --- |
| `requirements/data.txt` | `pandas`, `polars` | Derived component joins, authority tables, large transforms. |
| `requirements/schema.txt` | `pydantic`, `pandera`, `linkml` | Component models, tabular contracts, generated schemas. |
| `requirements/xml.txt` | `lxml`, `xmlschema` | ParlaMint/TEI and Akoma Ntoso generation and validation. |
| `requirements/rdf.txt` | `rdflib`, `pyshacl`, `linkml` | RDF, JSON-LD, SHACL, PROV-O, DCAT, SKOS. |
| `requirements/authority.txt` | `rapidfuzz` | Member, party, bill, motion, and alias matching. |
| `requirements/nlp.txt` | `spacy`, `stanza`, `conllu`, `pyconll` | NER, tokenization, UD/CoNLL-U, token alignment. |
| `requirements/ml.txt` | `scikit-learn`, `transformers`, `sentence-transformers`, `bertopic` | Topic classification, embeddings, exploratory models. |
| `requirements/metadata.txt` | `frictionless`, `rocrate`, `mlcroissant` | Frictionless Data Package, RO-Crate, Croissant metadata. |
| `requirements/dev.txt` | `ruff`, `ty`, `typos`, `zizmor`, `taplo` | CI quality, strict type checking, workflow-security linting, spelling, and TOML formatting. |

The policy authority is `manifests/dependency_extras_policy.json`, validated by `scripts/check_dependency_extras_policy.py`. The manifest records each optional group, the endpoint tracks that cite it, and the fields that endpoint validation manifests must carry: `dependency_groups`, `install_commands`, `tool_versions`, `library_versions`, `model_versions`, `lock_or_constraints`, `release_affecting_dependencies`, and `validation_command`.

## Dependency Rules

- Keep `requirements.txt` as the base runtime unless an existing production script imports the dependency.
- Add endpoint dependencies to grouped requirement files or package extras when implementation starts.
- Keep CI/developer tooling in `requirements/dev.txt` rather than the base runtime.
- Do not make GPU, transformer, or NLP model downloads part of the default test suite.
- Pin dependencies that affect generated release artifacts once an endpoint is published. The manifest policy value is `pin-before-release-artifact`.
- Prefer a lockfile or generated constraints file before expanding CI to heavier endpoint stacks.
- Record tool and model versions in each endpoint validation manifest.
- Keep optional group installation checks `deferred-until-implementation` until an endpoint track begins generating release-affecting artifacts.

## Endpoint Install Checks

Each endpoint implementation track must run and record the grouped install command from `manifests/dependency_extras_policy.json` before it generates public artifacts. Current planned groups are:

- `requirements/data.txt`
- `requirements/schema.txt`
- `requirements/xml.txt`
- `requirements/rdf.txt`
- `requirements/authority.txt`
- `requirements/nlp.txt`
- `requirements/ml.txt`
- `requirements/metadata.txt`
