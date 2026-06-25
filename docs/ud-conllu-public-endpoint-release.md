# Universal Dependencies / CoNLL-U Public Endpoint Release

## Decision

This track is release-ready as a manual-fixture sample-only public endpoint package under `release-ready-sample-public-endpoint`.

## Basis

- The existing UD / CoNLL-U package is a sample package and remains `sample-not-release`.
- validated speech-turn text is available for the sample-scoped endpoint release.
- the Stanza/spaCy comparison remains pending.
- the sample is manual-fixture based and makes no gold-standard UD annotation claim.

## Current Boundary

- Publish `samples/ud-conllu/parliament_sample.conllu`, `parliament_sample.alignments.json`, and `README.md` as sample-scoped public endpoint outputs.
- Keep the public claim sample-only and do not claim full UD / CoNLL-U corpus readiness.
- Keep the Stanza/spaCy comparison and gold-standard annotation claims deferred.

## Future Validation Requirements

- Corpus-wide UD / CoNLL-U output must run against normalized Hansard inputs before broad endpoint release claims are made.
- a completed Stanza/spaCy comparison must exist before model provenance can be treated as release-ready.
- public endpoint output must state machine-generated or reviewed status without overclaiming gold annotation.

## Outputs

- `manifests/ud_conllu_public_endpoint_validation.json`
- `samples/ud-conllu/parliament_sample.conllu`
- `samples/ud-conllu/parliament_sample.alignments.json`
- `samples/ud-conllu/README.md`
