# Track ud_conllu_public_endpoint_release_20260610 Context

Move UD / CoNLL-U from sample readiness to a scope-declared public endpoint package.

Repo-side builder/checker are implemented with gate `release-ready-sample-public-endpoint` after validated speech-turn text became available.
This remains sample-only manual-fixture evidence; Stanza/spaCy comparison is pending and there is no gold-standard UD annotation claim.

Current implementation surface:

- `schemas/ud_conllu_public_endpoint_validation.schema.json`
- `manifests/ud_conllu_public_endpoint_validation.json`
- `docs/ud-conllu-public-endpoint-release.md`
- `scripts/build_ud_conllu_public_endpoint.py`
- `scripts/check_ud_conllu_public_endpoint.py`
