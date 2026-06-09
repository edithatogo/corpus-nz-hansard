# Spec: Universal Dependencies / CoNLL-U Endpoint

## MoSCoW Requirements

### Must

- Define target text units for annotation.
- Record tokenizer, parser, model, language, and version metadata.
- Validate CoNLL-U parseability.
- Preserve token offsets back to source text.

### Should

- Support document-level text first and speech-turn text once validated.
- Compare Stanza and spaCy outputs on a small fixture before choosing defaults.

### Could

- Add manually reviewed evaluation samples.

### Won't

- Treat automated NLP annotations as corrected gold-standard UD trees without review.

## Acceptance Criteria

- CoNLL-U sample output, validator, alignment manifest, and model metadata exist.
