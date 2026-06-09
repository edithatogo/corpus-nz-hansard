# Dependency Policy

## Purpose

Keep the base corpus pipeline reproducible and lightweight while allowing endpoint-specific toolchains for XML, RDF, NLP, ML, and metadata work.

## Current Base Runtime

The current `requirements.txt` is the base runtime:

| Dependency | Purpose |
| --- | --- |
| `duckdb==1.5.3` | Local analytical database generation and validation. |
| `pyarrow` | Parquet and Arrow table generation. |
| `jsonschema>=4.22.0` | JSON Schema validation. |
| `requests>=2.32.0` | Zenodo and metadata API calls. |
| `huggingface_hub>=0.34.0` | Hugging Face dataset publication. |

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

## Dependency Rules

- Keep `requirements.txt` as the base runtime unless an existing production script imports the dependency.
- Add endpoint dependencies to grouped requirement files or package extras when implementation starts.
- Do not make GPU, transformer, or NLP model downloads part of the default test suite.
- Pin dependencies that affect generated release artifacts once an endpoint is published.
- Record tool and model versions in each endpoint validation manifest.
