# Public Release Checklist

## Required Before Upload

- [x] Confirm GitHub as code/review-package host.
- [x] Confirm Hugging Face as intended live dataset host.
- [x] Confirm Zenodo as intended DOI/archive host.
- [x] Assign review version `0.1.0-review.20260603`.
- [x] Confirm generated Parquet is uploaded to Hugging Face after credentialed publication.
- [x] Confirm DuckDB is treated as local-only regenerated output by default.
- [ ] Review `DATASET_CARD.md`.
- [ ] Review `docs/licensing-and-provenance.md`.
- [ ] Confirm no official endorsement is implied.
- [ ] Confirm source archive hash and row counts match manifests.
- [x] Confirm `manifests/record_schema_validation.json` passes with zero errors.
- [ ] Confirm limitations around party, member identity, and speech-turn segmentation are visible.
- [x] Confirm source ZIP is not redistributed by default.
- [x] Confirm non-authoritative speech-turn candidates are excluded from the initial public dataset.
- [ ] Run `python scripts/check_publication_readiness.py`.
- [ ] Add `HF_TOKEN` and run Hugging Face upload.
- [ ] Add `ZENODO_TOKEN` and `ARCHIVE_CREATORS_JSON`, then create Zenodo draft.

## Current Evidence

- Source inventory: `manifests/source_inventory.json`
- Schema discovery: `manifests/schema_discovery.json`
- Normalization validation: `manifests/normalization_validation.json`
- Record schema validation: `manifests/record_schema_validation.json`
- DuckDB validation: `manifests/duckdb_validation.json`
- Public release manifest: `manifests/public_dataset_release_manifest.json`

## Do Not Claim Yet

- Do not claim official Parliament endorsement.
- Do not claim speech-turn-level structure.
- Do not claim party-level analysis is directly supported.
- Do not claim full dataset public release has occurred.
- Do not claim a DOI exists until Zenodo publication is verified.
- Do not claim source ZIP redistribution is allowed.
- Do not claim DuckDB/search SQLite are public dataset artifacts unless they are explicitly uploaded and verified.
