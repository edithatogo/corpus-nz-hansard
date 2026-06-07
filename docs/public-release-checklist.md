# Public Release Checklist

## Required Before Upload

- [ ] Confirm final hosting target.
- [ ] Assign dataset version.
- [ ] Confirm whether generated Parquet is uploaded, regenerated, or packaged separately.
- [ ] Confirm DuckDB is included or treated as local-only generated output.
- [ ] Review `DATASET_CARD.md`.
- [ ] Review `docs/licensing-and-provenance.md`.
- [ ] Confirm no official endorsement is implied.
- [ ] Confirm source archive hash and row counts match manifests.
- [ ] Confirm `manifests/record_schema_validation.json` passes with zero errors.
- [ ] Confirm limitations around party, member identity, and speech-turn segmentation are visible.

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
- Do not claim public release has occurred.
