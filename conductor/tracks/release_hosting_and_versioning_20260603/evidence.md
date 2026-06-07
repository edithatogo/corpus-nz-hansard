# Evidence: Release Hosting and Versioning

## Phase 1

Status: complete.

Created:

- `VERSION`
- `RELEASE_NOTES.md`
- `docs/hosting-decision-matrix.md`

Version:

- `0.1.0-review.20260603`

Publication boundary:

- Local review package only.
- No upload occurred.
- No Git tag or commit was created.

## Phase 2

Status: complete.

### Red Phase

Command:

```powershell
python -m unittest tests.test_build_release_package
```

Result:

- Failed as expected before implementation.
- Failure reason: `ModuleNotFoundError: No module named 'scripts.build_release_package'`.

### Green Phase

Command:

```powershell
python -m unittest tests.test_build_release_package
```

Result:

- Passed.
- Test count: 1.

### Package Build

Command:

```powershell
python scripts\build_release_package.py --output-dir generated\release --package-name nz-hansard-corpus-0.1.0-review.20260603.zip
```

Result:

- Package: `generated/release/nz-hansard-corpus-0.1.0-review.20260603.zip`
- Manifest: `generated/release/nz-hansard-corpus-0.1.0-review.20260603.manifest.json`
- Files: 200
- Package SHA-256: `ccf031a71baa61ceda59bcd47d284c5ffd5fedf5cb8420155ad3446e0ee73640`
- Published: false

Validation:

- Package manifest parsed as JSON.
- Source ZIP excluded.
- `generated/parquet/hansard.parquet` excluded.
- `README.md` and `DATASET_CARD.md` included.

## Phase 3

Status: complete.

No upload or publication occurred. The review package is a local generated artifact and can be regenerated from tracked files.
