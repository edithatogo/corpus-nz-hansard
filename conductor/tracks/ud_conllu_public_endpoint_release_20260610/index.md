# Track ud_conllu_public_endpoint_release_20260610 Context

Move UD/CoNLL-U from sample output to a scope-declared public endpoint release.

Repo-side builder/checker are implemented, but the release is blocked until validated speech-turn text is available and the Stanza/spaCy comparison is complete. This remains sample-only evidence rather than a public endpoint release.

Current implementation surface:

- `schemas/ud_conllu_public_endpoint_validation.schema.json`
- `manifests/ud_conllu_public_endpoint_validation.json`
- `docs/ud-conllu-public-endpoint-release.md`
- `scripts/build_ud_conllu_public_endpoint.py`
- `scripts/check_ud_conllu_public_endpoint.py`
