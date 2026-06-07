# Evidence: Speech Turn Segmentation MVP

## Phase 1

Status: complete.

Created:

- `docs/speech-turn-segmentation-contract.md`
- `tests/test_segment_speech_turns.py`

### Red Phase

Command:

```powershell
python -m unittest tests.test_segment_speech_turns
```

Result:

- Failed as expected before implementation.
- Failure reason: `ModuleNotFoundError: No module named 'scripts.segment_speech_turns'`.

## Phase 2

Status: complete.

Created:

- `scripts/segment_speech_turns.py`
- `generated/parquet/hansard_speech_turns.parquet`
- `manifests/speech_turn_segmentation_validation.json`
- `docs/speech-turn-segmentation-report.md`

### Green Phase

Command:

```powershell
python -m unittest tests.test_segment_speech_turns
```

Result:

- Passed.
- Test count: 3.

### Full Segmentation Command

Command:

```powershell
python scripts\segment_speech_turns.py --input generated\parquet\hansard.parquet --output generated\parquet\hansard_speech_turns.parquet --validation manifests\speech_turn_segmentation_validation.json --batch-size 1000
```

Result:

- Documents read: 193,922
- Candidate turns written: 439
- Documents with turns: 360
- Documents without turns: 193,562
- Confidence counts: `medium = 439`
- Authoritative: false

Turns by document type:

| Document type | Candidate turns |
| --- | ---: |
| `Hansard - daily` | 149 |
| `Hansard - debate` | 149 |
| `Hansard - question` | 56 |
| `Hansard - speech` | 84 |
| `Hansard - vote` | 1 |

## Phase 3

Status: complete.

Final readiness:

- The output is useful as a conservative review artifact.
- It is not suitable for authoritative speech attribution.
- Stronger segmentation should be a later track.
