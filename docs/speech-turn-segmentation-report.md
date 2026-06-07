# Speech Turn Segmentation Report

## Status

Heuristic MVP. Not authoritative.

## Input

- `generated/parquet/hansard.parquet`
- Documents read: 193,922

## Output

- `generated/parquet/hansard_speech_turns.parquet`
- Validation: `manifests/speech_turn_segmentation_validation.json`

## Method

`tab_colon_marker_v1` splits document content on tab characters and emits a turn only when it finds a clear `speaker : speech` marker.

## Results

- Candidate turns written: 439
- Documents with candidate turns: 360
- Documents without candidate turns: 193,562
- Confidence categories: `medium` only
- Authoritative: false

Turns by document type:

| Document type | Candidate turns |
| --- | ---: |
| `Hansard - daily` | 149 |
| `Hansard - debate` | 149 |
| `Hansard - question` | 56 |
| `Hansard - speech` | 84 |
| `Hansard - vote` | 1 |

## Interpretation

The low turn count is expected. This MVP intentionally avoids aggressive segmentation and emits only obvious tab-colon candidates. It is useful for reviewing source formatting and designing a stronger future segmenter, not for production-grade speech attribution.

## Next Work

- Add Hansard-specific procedural parsing.
- Detect speaker names embedded in content without tab-colon separation.
- Normalize member names against a member register.
- Add confidence calibration with manually reviewed samples.
