# Evidence: Universal Dependencies / CoNLL-U Endpoint

## Annotation Units

Evidence for the UD / CoNLL-U Sample Package:

- Manifest: `manifests/ud_conllu_validation_manifest.json`
- Model metadata: `manifests/ud_conllu_model_metadata.json`
- Sample output: `samples/ud-conllu/parliament_sample.conllu`
- Alignment manifest: `samples/ud-conllu/parliament_sample.alignments.json`
- Sample package README: `samples/ud-conllu/README.md`
- Mapping doc: `docs/ud-conllu-mapping.md`

The sample package is `sample-not-release` and remains `blocked-pending-validated-components`.
Source offsets are preserved in the alignment manifest and CoNLL-U `MISC` column.
`stanza` and `spacy` remain prototype comparison candidates.

## Model Metadata

The model metadata records the tokenizer, parser, annotation family, language, and prototype comparison candidates.

## CoNLL-U Validation

The CoNLL-U sample validates as a single speech-turn annotation row set with preserved token IDs and parseable 10-column lines.

## Source-Offset Alignment

The alignment manifest preserves source offsets for every token and maps them back to the source text.
