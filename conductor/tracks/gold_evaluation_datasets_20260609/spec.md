# Spec: Gold Evaluation Datasets

## MoSCoW Requirements

### Must

- Define evaluation samples for member resolution, party attribution, speech turns, votes, and topic coding.
- Include positive, negative, ambiguous, unresolved, and excluded examples.
- Record sampling frame, review status, reviewer, reviewed date, and label provenance.

### Should

- Support precision, recall, ambiguity, and regression checks.
- Keep gold/evaluation data small enough for Git when licensing allows.

### Could

- Add stratified samples by parliament, document type, and date range.

### Won't

- Treat model-generated labels as gold without review.

## Acceptance Criteria

- Evaluation schemas, fixtures, and validation tests exist before derived artifacts are published.
