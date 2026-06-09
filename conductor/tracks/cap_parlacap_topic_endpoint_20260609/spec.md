# Spec: CAP / ParlaCAP Topic Endpoint

## MoSCoW Requirements

### Must

- Declare the CAP codebook version used.
- Link every topic assignment to a source document, proceeding item, or speech turn.
- Distinguish human-coded, rule-coded, and model-coded labels.
- Validate topic codes against the declared codebook.

### Should

- Generate ParlaCAP-compatible outputs when speech turns are validated.
- Add baseline classifiers only after labelled training/evaluation data is defined.

### Could

- Add exploratory topic modelling outputs marked as non-authoritative.

### Won't

- Publish model-coded topics as validated research labels without evaluation evidence.

## Acceptance Criteria

- Topic schema, codebook metadata, validation manifest, and sample outputs exist.

## Dependencies

- Depends on gold/evaluation datasets, CAP codebook provenance, speech/proceeding units, NZ parliamentary procedure model, and release ladder.
