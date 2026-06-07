# Schema Discovery Report

## Source

- Archive: `2024-09-06 Hansard Extract from DocumentsDB.zip`
- Machine-readable report: `manifests/schema_discovery.json`
- Discovery command:

```powershell
python scripts\discover_schema.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output manifests\schema_discovery.json --sample-rows 5
```

## Summary

- CSV files inspected: 8
- Total rows counted: 193,922
- Header signatures: 1
- Delimiter: comma
- Headers are consistent across all files.
- Encoding differs by file: `Hansard-47.csv` is `cp1252`; `Hansard-48.csv` through `Hansard-54.csv` are `utf-16`.

## Columns

All 8 files contain the same 11 columns:

1. `ParliamentNumber`
2. `ParliamentDocumentId`
3. `DocumentType`
4. `Title`
5. `AbbreviatedTitle`
6. `Status`
7. `Content`
8. `MemberOfParliament`
9. `Portfolio`
10. `LastModified`
11. `DocumentContentDate`

## Row Counts

| File | Encoding | Rows |
| --- | --- | ---: |
| `Hansard-47.csv` | `cp1252` | 24,378 |
| `Hansard-48.csv` | `utf-16` | 19,709 |
| `Hansard-49.csv` | `utf-16` | 23,877 |
| `Hansard-50.csv` | `utf-16` | 39,803 |
| `Hansard-51.csv` | `utf-16` | 34,808 |
| `Hansard-52.csv` | `utf-16` | 21,171 |
| `Hansard-53.csv` | `utf-16` | 23,402 |
| `Hansard-54.csv` | `utf-16` | 6,774 |

## Candidate Normalized Fields

- Parliamentary term: `ParliamentNumber`
- Document ID: `ParliamentDocumentId`
- Document type: `DocumentType`
- Topic/title: `Title`, `AbbreviatedTitle`
- Status: `Status`
- Text: `Content`
- Speaker/member field: `MemberOfParliament`
- Portfolio: `Portfolio`
- Modified timestamp: `LastModified`
- Content date: `DocumentContentDate`

## Limitations and Follow-Up

- No explicit `Party` column exists in the source schema.
- `MemberOfParliament` may contain multiple semicolon-separated names and should be treated as a multi-value field during normalization design.
- `Content` contains embedded tab-like separators and speech text; normalization must preserve source text while defining derived speaker/speech segmentation separately.
- `LastModified` and `DocumentContentDate` need date parsing validation in the normalization phase.
