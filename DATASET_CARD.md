# NZ Hansard Corpus Dataset Card

## Dataset Summary

This workspace prepares a document-level corpus from New Zealand Hansard CSV extracts. The current pipeline inventories the source ZIP, discovers schema, normalizes document-level records to Parquet, and builds a local DuckDB analytical database.

This card describes the local generated dataset. It does not mean the dataset has been publicly uploaded or endorsed by New Zealand Parliament.

## Source

- Source archive: `2024-09-06 Hansard Extract from DocumentsDB.zip`
- Source archive SHA-256: `2ac02c0042a4fb291fd8e401db5f469de2539e42c9e07c4c72eca16be9a17299`
- Source files: `Hansard-47.csv` through `Hansard-54.csv`
- Source scope: New Zealand Parliament Hansard records for Parliament numbers 47 through 54, as present in the supplied DocumentsDB extract.

## Legal and Provenance Notes

New Zealand Parliament's Parliamentary Practice material states that Hansard is the official report of debates in the House, and that no copyright exists in New Zealand Parliamentary Debates/Hansard. See `docs/licensing-and-provenance.md` for source links and caveats.

This dataset card does not provide legal advice and does not represent final publication approval.

## Dataset Structure

The normalized Parquet dataset is document-level, not speech-turn-level.

Columns:

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

## Current Counts

- Source files: 8
- Source/schema-discovered rows: 193,922
- Normalized Parquet rows: 193,922
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
- Preparation for public dataset packaging.
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
- Licensing/provenance has been checked against official public guidance, but public release still requires final human review.
- Generated DuckDB output may include a `.wal` file on OneDrive-backed workspaces.

## Regeneration

See `README.md` and `docs/pipeline-handoff.md` for reproducible commands.
