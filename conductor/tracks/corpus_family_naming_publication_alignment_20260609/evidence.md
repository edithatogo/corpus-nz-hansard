# Evidence: Corpus Family Naming And Publication Alignment

## Initial Evidence

Status: opened on 2026-06-09.

This track records naming preferences, sibling-project cross-references, and publication-environment alignment requirements across GitHub, Hugging Face, Zenodo, OSF, and future metadata surfaces.

## Implementation Evidence

Implemented a self-contained alignment ledger and validator inside the Worker 5 ownership boundary:

- `manifests/corpus_family_publication_alignment.json` records the preferred `corpus-nz-hansard` and `corpus-nz-legislation` labels, stable public-surface URLs, non-migration decisions, OSF/future metadata claim boundaries, DOI update rules, and documentation gates.
- `schemas/corpus_family_publication_alignment.schema.json` validates the alignment ledger shape and required environment identifiers.
- `docs/corpus-family-naming-publication-alignment.md` documents the family naming standard, hosting matrix, Mermaid alignment diagrams, environment gates, and DOI update rules.
- `scripts/check_corpus_family_alignment.py` validates schema conformance, agreement with `manifests/public_dataset_release_manifest.json`, agreement with `manifests/public_surface_audit.json`, required documentation terms, and this evidence file.
- `tests/test_corpus_family_alignment.py` covers the ledger content and checker.

## Public-Surface Readback Incorporated

The alignment ledger reuses the current public-surface audit evidence:

- GitHub remains `https://github.com/edithatogo/corpus-nz-hansard` with decision `keep-existing-url`.
- Hugging Face remains `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus` with decision `keep-existing-url`; viewer/access health remains a release gate.
- Zenodo remains `https://zenodo.org/records/20595194` and DOI `10.5281/zenodo.20595194` with decision `keep-existing-url`.
- OSF remains `not-yet-published` pending `osf_optional_mirror_policy_20260609`.
- Croissant, RO-Crate, Frictionless, DCAT, PROV-O, and other metadata surfaces remain `not-yet-published` pending `sota_metadata_packages_20260609`.

## Focused validation

Passed on 2026-06-10:

```powershell
python -m unittest tests.test_corpus_family_alignment
python scripts/check_corpus_family_alignment.py
```

## Scope Boundary

This worker did not edit `conductor/tracks.md`, `Makefile`, CI, or shared quality-gate files. Registry promotion and shared quality-gate wiring remain outside Worker 5 ownership.
