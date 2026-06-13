# Historical Coverage Audit

## Coverage Claim Boundary

This repository has verified the supplied DocumentsDB extract, not full historical New Zealand Hansard completeness.

Verified claims:

- The source archive is `2024-09-06 Hansard Extract from DocumentsDB.zip`.
- The source archive SHA-256 is `2ac02c0042a4fb291fd8e401db5f469de2539e42c9e07c4c72eca16be9a17299`.
- The archive inventory contains eight CSV members, `Hansard-47.csv` through `Hansard-54.csv`.
- The normalized document-level output preserves 193,922 rows from those source files with zero normalization warnings.

Partial claims:

- Parliament numbers 47 through 54 are present as source-file partitions.
- Document categories observed in sampled source rows include daily, debate, question, speech, and vote records.
- Presence of these files and sampled categories does not prove that every sitting, proceeding, document type, vote, question, debate, or speech for those parliaments is complete.

Unknown claims:

- Complete historical Hansard coverage across all New Zealand parliamentary periods has not been established.
- Sitting-date and proceeding completeness have not been reconciled against an official sitting calendar, Daily Progress ledger, Order Paper history, or current/historical Hansard website retrieval.

Excluded claims:

- Records before `Hansard-47.csv` are outside the current canonical dataset.
- Records after the supplied 2024-09-06 archive snapshot are outside the current canonical dataset.
- The current dataset must not be described as a full historical NZ Hansard corpus.

## Source File Coverage

| Parliament | Source file | Rows | Status |
| --- | --- | ---: | --- |
| 47 | `Hansard-47.csv` | 24,378 | Partial |
| 48 | `Hansard-48.csv` | 19,709 | Partial |
| 49 | `Hansard-49.csv` | 23,877 | Partial |
| 50 | `Hansard-50.csv` | 39,803 | Partial |
| 51 | `Hansard-51.csv` | 34,808 | Partial |
| 52 | `Hansard-52.csv` | 21,171 | Partial |
| 53 | `Hansard-53.csv` | 23,402 | Partial |
| 54 | `Hansard-54.csv` | 6,774 | Partial |

`Partial` means the file exists, its hash and row count are recorded, and its rows are preserved in the normalized output. It does not mean the file has been proven complete against external parliamentary calendars or official Hansard publication ledgers.

## Authority Cross-Check Status

`manifests/authority_sources.json` now identifies source candidates for the next historical reconciliation step:

- `nz-parliament-hansard-current`
- `nz-parliament-order-paper`
- `nz-parliament-daily-progress`
- `nzlii-historical-bills`
- `electoral-commission-election-results`

Those sources are available for follow-up reconciliation, but this track does not complete a sitting-level historical comparison. Any endpoint or release surface that describes coverage must cite `manifests/historical_coverage_audit.json` and preserve the distinction between supplied archive coverage and historical Hansard completeness.

The current reconciliation inventory also includes the historic journals archive,
sessional journals archive, and indexes to the journals so that older periods
can be compared against the official parliamentary record rather than only the
live parliamentary business entrypoints.

The comparison contract itself is recorded in
`manifests/historical_sitting_reconciliation.json` and documented in
`docs/historical-sitting-reconciliation.md`.
