# Universal Dependencies / CoNLL-U Mapping Notes

This package is a maintainer-review sample, not a release artifact.

References used by this sample package:

- `manifests/ud_conllu_validation_manifest.json`
- `manifests/ud_conllu_model_metadata.json`
- `samples/ud-conllu/parliament_sample.conllu`
- `samples/ud-conllu/parliament_sample.alignments.json`
- `fixtures/neutral_components.json`

## Annotation Scope

- Target text unit: speech turn
- Source component: `nzhc-component-0000000000000005`
- Source stable ID: `HansS_20240625_067140000`

## Notes

- source offsets are preserved in the alignment manifest and the CoNLL-U MISC column.
- The sample keeps punctuation separate so the parse is CoNLL-U compatible.
- `stanza` and `spacy` remain prototype comparison candidates recorded in model metadata.
- This sample is `sample-not-release` and remains `blocked-pending-validated-components`.
