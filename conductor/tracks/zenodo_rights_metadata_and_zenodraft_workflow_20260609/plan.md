# Plan: Zenodo Rights Metadata And Zenodraft Workflow

## Phase 1: Rights and metadata audit

- [x] Audit canonical and superseded Zenodo records, license, files, creators, related identifiers, concept DOI, and version DOI.
- [x] Separate rights for repository code, docs, manifests, source text, normalized Parquet, generated metadata, and archive bundle.
- [x] Decide whether Zenodo license metadata should remain other-open, switch to a more specific license, or use another rights statement with scope notes.
- [x] Align `README.md`, `DATASET_CARD.md`, `CITATION.cff`, `NOTICE.md`, and Zenodo metadata text.

## Phase 2: Zenodraft adoption/evaluation

- [x] Add `zenodraft` evaluation notes from `https://github.com/zenodraft/zenodraft`.
- [x] Decide between `npx zenodraft`, pinned npm install, or Docker invocation in CI.
- [x] Document Node >= 20 and npm >= 10 requirements if adopted.
- [x] Map existing `ZENODO_TOKEN` / `ZENODO_SANDBOX_TOKEN` secrets to `ZENODO_ACCESS_TOKEN` / `ZENODO_SANDBOX_ACCESS_TOKEN` only within the relevant step.
- [x] Generate local `.zenodo.json` metadata and validate it with a repo-side Zenodo metadata policy check.
- [x] Prove sandbox draft creation in Zenodo Sandbox with a `deposit:write` token.
- [x] Prove file upload with generated metadata package files.
- [x] Prove metadata update in the sandbox draft.
- [x] Capture prereserved DOI/details readback from the sandbox draft.

## Phase 3: Protected publication gate

- [x] Keep `zenodraft deposition publish` out of ordinary upload/update jobs.
- [x] Require GitHub environment protection and reviewer approval before production publish.
- [x] Record production publication evidence only after draft review.

## Verification

- [x] Metadata JSON parses.
- [x] Track is registered in `conductor/tracks.md`.
- [x] Sandbox proof gate and token mapping are documented before production use.
