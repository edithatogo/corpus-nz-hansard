# Evidence: Public Dataset Readiness

## Source References

- New Zealand Parliament, Parliamentary Practice in New Zealand, chapter 12. Lines inspected during setup include statements that Hansard is the official report, is published digitally, and that no copyright exists in New Zealand Parliamentary Debates/Hansard.

## Phase 1

Status: complete.

Created:

- `DATASET_CARD.md`
- `docs/licensing-and-provenance.md`
- `docs/public-release-checklist.md`

Publication boundary:

- Public release documentation is prepared for review.
- No upload or publication occurred.
- No official endorsement is claimed.

## Phase 2

Status: complete.

### Red Phase

Command:

```powershell
python -m unittest tests.test_public_release_manifest
```

Result:

- Failed as expected before implementation.
- Failure reason: `ModuleNotFoundError: No module named 'scripts.build_public_release_manifest'`.

### Green Phase

Command:

```powershell
python -m unittest tests.test_public_release_manifest
```

Result:

- Passed.
- Test count: 2.

### Release Manifest

Command:

```powershell
python scripts\build_public_release_manifest.py --output manifests\public_dataset_release_manifest.json
```

Result:

- Output: `manifests/public_dataset_release_manifest.json`
- Publication status: `prepared_for_review`
- Published: `false`
- Rows: 193,922

## Phase 3

Status: complete.

Final readiness position:

- Prepared for public release review.
- Not published.
- Final human licensing/provenance and hosting review still required.
