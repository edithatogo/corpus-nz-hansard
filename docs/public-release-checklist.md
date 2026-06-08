# Public Release Checklist

## Required Before Upload

- [x] Confirm GitHub as code/review-package host.
- [ ] Confirm Hugging Face as live dataset host.
- [ ] Confirm Zenodo as DOI/archive host.
- [x] Assign review version `0.1.0-review.20260603`.
- [ ] Confirm whether generated Parquet is uploaded, regenerated, or packaged separately.
- [ ] Confirm DuckDB is included or treated as local-only generated output.
- [ ] Review `DATASET_CARD.md`.
- [ ] Review `docs/licensing-and-provenance.md`.
- [ ] Confirm no official endorsement is implied.
- [ ] Confirm source archive hash and row counts match manifests.
- [x] Confirm `manifests/record_schema_validation.json` passes with zero errors.
- [ ] Confirm limitations around party, member identity, and speech-turn segmentation are visible.
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
