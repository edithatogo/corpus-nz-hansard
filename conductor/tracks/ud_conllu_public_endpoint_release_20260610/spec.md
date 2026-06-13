# Spec: UD/CoNLL-U Public Endpoint Release

## Goal

Move UD/CoNLL-U output from sample package to a validated NLP endpoint release.

## MoSCoW Requirements

### Must

- Pin tokenizer, parser, language model, versions, and runtime options.
- Preserve token, sentence, document, and source-span alignment.
- Validate CoNLL-U format, offset fidelity, and model provenance.
- Declare coverage, exclusions, and whether output is machine-generated or reviewed.

### Should

- Compare parser output against reviewed fixtures or benchmark samples.
- Feed NIF/RDF linguistic annotation views.

### Could

- Release tokenization-only views before dependency parsing if quality differs.

### Won't

- Claim gold-standard UD annotation without human-reviewed validation.

## Acceptance Criteria

- Endpoint output validates, reproduces, and includes model cards/manifests.
- Docs state machine-generated status and known limitations.
