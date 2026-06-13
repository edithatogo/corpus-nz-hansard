# Spec: Validated Speech-Turn Component Release

## Goal

Promote speech-turn candidates into a validated derived component only when the candidate artifact and validated member identity are both available.

## MoSCoW Requirements

### Must

- Preserve document identifiers, turn indices, speaker candidates, selectors, and source linkage.
- Separate segmentation confidence from speaker identity confidence.
- Gate promotion on candidate data and validated member identity.
- Emit schema, validation manifest, review queue, docs, and release decision.

### Should

- Validate across hard colon-marker, embedded-heading, no-speaker fallback, and multi-speaker cases.
- Preserve a review queue for unresolved speaker identity cases.
- Carry a turn ID that is stable within the corpus release surface.

### Could

- Publish a sample-only validated preview once member identity becomes available.

### Won't

- Promote heuristic candidates as authoritative without a validated member identity gate.
- Change the document-level `v0.1.0` corpus.

## Acceptance Criteria

- The validated track has explicit schema, docs, manifest, and checks.
- The release gate stays blocked in the current workspace and states the blocking reason clearly.
