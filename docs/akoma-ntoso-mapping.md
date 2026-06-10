# Akoma Ntoso Mapping Notes

This package is a maintainer-review sample, not a release artifact.

References used by this sample package:

- `manifests/akoma_ntoso_validation_manifest.json`
- `samples/akoma-ntoso/Akoma-Ntoso.sample.xml`
- `fixtures/neutral_components.json`

## Profile

- Akoma Ntoso namespace: `http://docs.oasis-open.org/legaldocml/ns/akn/3.0`
- Profile subset: debate-oriented sample with `doc`, `meta`, `body`, `debate`, `speech`, and `vote`
- Release boundary: `sample-not-release`

## Mapping

- `sittings` provide the generated document date and sitting context.
- `proceeding_items` provide the debate heading and source-order anchor.
- `speech_turns` provide the speech body and speaker attribution.
- `members` and `parties` provide speaker and organization references.
- `motions` provide the motion heading for the vote block.
- `votes` provide vote type, outcome, and counts.
- `bills` provide the bill title and stage note.

The mapping notes here are deliberately narrow and are not schema validation evidence.

## NZ-Specific Limits

- The sample preserves source order and source provenance only for a narrow fixture set.
- This package does not assert full legislative-document coverage for New Zealand Parliament.
- It remains `blocked-pending-validated-components` until validated member, party, speech-turn, motion, and vote components exist.
