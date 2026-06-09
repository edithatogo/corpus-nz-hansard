# Spec: ParlaMint-NZ Endpoint

## MoSCoW Requirements

### Must

- Generate ParlaMint-compatible TEI XML from neutral components.
- Produce metadata files and a representative sample package.
- Validate XML well-formedness and declared ParlaMint schema requirements.
- Ensure speaker and party references resolve to validated component metadata.

### Should

- Record NZ-specific encoding decisions for sittings, questions, votes, and procedural text.
- Add sample files suitable for maintainer review.
- Track Parla-CLARIN schema feedback separately from corpus data publication.

### Could

- Add optional linguistic annotation exports when UD/CoNLL-U artifacts exist.

### Won't

- Claim ParlaMint-NZ readiness until validation and maintainer-facing samples exist.
- Make ParlaMint fields the neutral core schema.

## Acceptance Criteria

- ParlaMint-NZ generator, sample output, validation manifest, and mapping notes exist.
- Generated samples trace every derived value back to neutral components.
