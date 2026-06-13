# Evidence: UD/CoNLL-U Public Endpoint Release

Status: blocked.

Implemented artifacts:

- `schemas/ud_conllu_public_endpoint_validation.schema.json`
- `manifests/ud_conllu_public_endpoint_validation.json`
- `docs/ud-conllu-public-endpoint-release.md`
- `scripts/build_ud_conllu_public_endpoint.py`
- `scripts/check_ud_conllu_public_endpoint.py`
- `tests/test_ud_conllu_public_endpoint.py`

Validation evidence:

- `python scripts/build_ud_conllu_public_endpoint.py`
- `python scripts/check_ud_conllu_public_endpoint.py`
- `python -m unittest tests.test_ud_conllu_public_endpoint`

Release boundary:

- The current UD/CoNLL-U package remains a maintainer-review sample, not a public endpoint release.
- Validated speech-turn text is not yet available for public endpoint output.
- The Stanza/spaCy comparison remains pending.
