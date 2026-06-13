# Spec: Speech-Act And Procedure Classifiers

## Goal

Add classifiers for speech acts, question/answer structure, interjections, procedural rulings, and debate segments.

## MoSCoW Requirements

### Must

- Depend on validated speech-turn and proceeding components.
- Define labels, training/evaluation data, provenance, model versions, confidence, and reviewed status.
- Preserve selectors and source links.

### Should

- Include benchmark metrics and confusion analysis.
- Support human-review correction files.

### Could

- Publish exploratory labels before validated labels if clearly scoped.

### Won't

- Claim authoritative procedural classification from unvalidated model output.

## Acceptance Criteria

- Classifier outputs are gated by speech-turn readiness and labelled by validation status.
