# Plan: Zenodo Rights Metadata And Zenodraft Workflow

## Phase 1: Rights and metadata audit

- [ ] Audit canonical and superseded Zenodo records, license, files, creators, related identifiers, concept DOI, and version DOI.
- [ ] Separate rights for repository code, docs, manifests, source text, normalized Parquet, generated metadata, and archive bundle.
- [ ] Decide whether Zenodo license metadata should remain other-open, switch to a more specific license, or use another rights statement with scope notes.
- [ ] Align `README.md`, `DATASET_CARD.md`, `CITATION.cff`, `NOTICE.md`, and Zenodo metadata text.

## Phase 2: Zenodraft adoption/evaluation

- [ ] Add `zenodraft` evaluation notes from `https://github.com/zenodraft/zenodraft`.
- [ ] Decide between `npx zenodraft`, pinned npm install, or Docker invocation in CI.
- [ ] Document Node >= 20 and npm >= 10 requirements if adopted.
- [ ] Map existing `ZENODO_TOKEN` / `ZENODO_SANDBOX_TOKEN` secrets to `ZENODO_ACCESS_TOKEN` / `ZENODO_SANDBOX_ACCESS_TOKEN` only within the relevant step.
- [ ] Generate local `.zenodo.json` metadata and validate it with `zenodraft metadata validate .zenodo.json`.
- [ ] Prove sandbox draft creation or version creation with `zenodraft deposition create concept --sandbox` or `zenodraft deposition create version --sandbox <concept_id>`.
- [ ] Prove file upload with `zenodraft file add --sandbox`.
- [ ] Prove metadata update with `zenodraft metadata update --sandbox`.
- [ ] Capture prereserved DOI/details with `zenodraft deposition show prereserved --sandbox` and `zenodraft deposition show details --sandbox`.

## Phase 3: Protected publication gate

- [ ] Keep `zenodraft deposition publish` out of ordinary upload/update jobs.
- [ ] Require GitHub environment protection and reviewer approval before production publish.
- [ ] Record production publication evidence only after draft review.

## Verification

- [ ] Metadata JSON parses.
- [ ] Track is registered in `conductor/tracks.md`.
- [ ] Sandbox proof and token mapping are documented before production use.
