# Universal Dependencies / CoNLL-U Public Endpoint Release

## Decision

This track is implemented as a blocked public endpoint release surface and remains sample-only evidence.

## Basis

- The existing UD / CoNLL-U package is a sample package and remains `sample-not-release`.
- validated speech-turn text is not yet available for a public endpoint release.
- the Stanza/spaCy comparison remains pending.
- the sample is manual-fixture based and not gold-standard UD annotation.

## Current Boundary

- Keep `samples/ud-conllu/parliament_sample.conllu`, `parliament_sample.alignments.json`, and `README.md` as sample-package evidence, not public endpoint output.
- Keep `manifests/ud_conllu_public_endpoint_validation.json` blocked until the dependent validation evidence is available.

## Future Validation Requirements

- validated speech-turn text must exist before tokenization and alignment can be treated as release-ready.
- a completed Stanza/spaCy comparison must exist before model provenance can be treated as release-ready.
- public endpoint output must state machine-generated or reviewed status without overclaiming gold annotation.

## Outputs

- `manifests/ud_conllu_public_endpoint_validation.json`
- `samples/ud-conllu/parliament_sample.conllu`
- `samples/ud-conllu/parliament_sample.alignments.json`
- `samples/ud-conllu/README.md`
