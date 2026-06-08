# NZ Hansard Corpus Dataset Card

## Dataset Summary

This workspace prepares a document-level corpus from New Zealand Hansard CSV extracts. The current pipeline inventories the source ZIP, discovers schema, normalizes document-level records to Parquet, validates a machine-readable record schema, and builds local DuckDB/search artifacts.

This card describes the published review-stage dataset. Publication does not imply endorsement by New Zealand Parliament.

## Published Locations

- Hugging Face dataset: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`
- Zenodo record: `https://zenodo.org/records/20591997`
- DOI: `https://doi.org/10.5281/zenodo.20591997`
- GitHub repository: `https://github.com/edithatogo/corpus-nz-hansard`
- GitHub review release: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0-review.20260603`

## Source

- Source archive: `2024-09-06 Hansard Extract from DocumentsDB.zip`
- Source archive SHA-256: `2ac02c0042a4fb291fd8e401db5f469de2539e42c9e07c4c72eca16be9a17299`
- Source files: `Hansard-47.csv` through `Hansard-54.csv`
- Source scope: New Zealand Parliament Hansard records for Parliament numbers 47 through 54, as present in the supplied DocumentsDB extract.

## Legal and Provenance Notes

New Zealand Parliament's Parliamentary Practice material states that Hansard is the official report of debates in the House, and that no copyright exists in New Zealand Parliamentary Debates/Hansard. See `docs/licensing-and-provenance.md` for source links and caveats.

This dataset card does not provide legal advice.

## Dataset Structure

The normalized Parquet dataset is document-level, not speech-turn-level.

Columns:

- `stable_id`
- `jurisdiction`
- `country`
- `source`
- `source_archive`
- `source_file`
- `source_row_number`
- `parliament_number`
- `parliament_document_id`
- `document_type`
- `title`
- `abbreviated_title`
- `status`
- `content`
- `member_of_parliament_raw`
- `member_of_parliament_count`
- `portfolio_raw`
- `last_modified`
- `document_content_date`
- `language`
- `text_sha256`
- `source_hash`
- `pipeline_version`

## Current Counts

- Source files: 8
- Source/schema-discovered rows: 193,922
- Normalized Parquet rows: 193,922
- Record schema validation errors: 0
- DuckDB rows: 193,922
- Normalization warnings: 0

Rows by Parliament:

| Parliament | Rows |
| --- | ---: |
| 47 | 24,378 |
| 48 | 19,709 |
| 49 | 23,877 |
| 50 | 39,803 |
| 51 | 34,808 |
| 52 | 21,171 |
| 53 | 23,402 |
| 54 | 6,774 |

## Intended Uses

- Local research over document-level Hansard text.
- Corpus-quality checks and exploratory analysis.
- Reproducible use of the public review-stage dataset.
- Preparation for reporting, semantic model, or search/RAG tracks.

## Out-of-Scope Uses

- Treating `member_of_parliament_raw` as a resolved member identity.
- Treating this MVP as a structured speech-turn corpus.
- Inferring party membership directly from this dataset.
- Claiming the dataset has been officially endorsed by Parliament.

## Known Limitations

- No explicit source `Party` column exists.
- `MemberOfParliament` is raw and may contain multiple semicolon-separated names.
- `Content` is document-level text and may contain embedded separators.
- Licensing/provenance has been checked against official public guidance, but users should review the linked provenance notes for their own use case.
- Generated DuckDB output may include a `.wal` file on OneDrive-backed workspaces.

## Distribution Policy

Initial public distribution policy:

- The source ZIP is not redistributed by default. Publication workflows require `SOURCE_ARCHIVE_URL` and verify the source archive SHA-256 before rebuilding.
- Hugging Face hosts the normalized document-level Parquet dataset.
- Zenodo hosts the citable archive and DOI record.
- DuckDB and SQLite search outputs are treated as regenerated/local convenience artifacts unless a reviewer explicitly asks for prebuilt database files.
- Non-authoritative speech-turn candidates are not part of the initial public dataset.

## Regeneration

See `README.md` and `docs/pipeline-handoff.md` for reproducible commands.
