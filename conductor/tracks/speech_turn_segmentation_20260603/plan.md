# Plan: Speech Turn Segmentation MVP

## Phase 1: Contract and Tests

- [x] Task: Document segmentation contract.
    - [x] Define output columns and confidence levels.
    - [x] Record heuristic limitations.
- [x] Task: Add fixture-based tests.
    - [x] Test colon-marker segmentation.
    - [x] Test no-turn fallback behavior.

## Phase 2: Implementation and Validation

- [x] Task: Implement segmentation script.
    - [x] Read normalized Parquet.
    - [x] Write generated speech-turn Parquet.
    - [x] Emit validation JSON.
- [x] Task: Run full generated segmentation.
    - [x] Validate row counts and confidence categories.
    - [x] Record evidence.

## Phase 3: Closure

- [x] Task: Final segmentation readiness review.
    - [x] Confirm heuristic scope.
    - [x] Update Conductor registry.
