# Zenodo Rights Metadata and Zenodraft Evaluation

This document records the rights metadata decision and the formal `zenodraft` evaluation for `corpus-nz-hansard`.

## Rights scope

| Component | Rights / publication posture |
| --- | --- |
| repository code | Original project material, MIT licensed. |
| documentation | Original project material, MIT licensed unless it quotes external source text. |
| manifests | Original project material, MIT licensed; used for reproducibility and audit evidence. |
| source text | New Zealand Parliamentary Debates/Hansard material from the supplied DocumentsDB extract; documentation records the Parliament provenance statement that no copyright exists in New Zealand Parliamentary Debates/Hansard. |
| normalized Parquet | Derived normalized document-level dataset; published with provenance caveats and no official endorsement claim. |
| generated metadata | Original project material generated from repository manifests and public release metadata. |
| archive bundle | Mixed release bundle containing derived data, code, docs, schemas, manifests, license, notice, and provenance notes; the source ZIP is not redistributed. |

## Zenodo metadata decision

The Zenodo license field remains `other-open` for this mixed archive bundle. A narrower license would overstate the scope of the MIT license because the archive contains both original repository materials and derived Hansard text. The descriptive rights text in `.zenodo.json`, `NOTICE.md`, and `docs/licensing-and-provenance.md` is the controlling scope note.

The canonical `.zenodo.json` records:

- title `NZ Hansard Corpus`;
- upload type `dataset`;
- version `0.1.0`;
- publication date `2026-06-08`;
- license `other-open`;
- DOI and concept DOI related identifiers;
- GitHub repository and release related identifiers;
- Hugging Face dataset related identifier;
- source ZIP non-redistribution, no official endorsement, source-text provenance, and MIT scope notes in the description.

## Zenodraft evaluation

The evaluated tool is `zenodraft/action@0.13.3`, from `https://github.com/zenodraft/action`. Its documented behavior matches this repository's safety requirements:

- it accepts Zenodo metadata from `.zenodo.json`;
- it supports Zenodo Sandbox with `sandbox: true`;
- it defaults `publish` to false, and this repository would keep `publish: false` for draft/update jobs;
- it expects `ZENODO_ACCESS_TOKEN` for production and `ZENODO_SANDBOX_ACCESS_TOKEN` for sandbox.

Adoption decision: defer migration from the existing Python REST scripts until a sandbox token is available and a maintainer explicitly requests migration. The current scripts are already covered by tests and keep draft upload/update separate from publication.

## Candidate sandbox workflow shape

Use Node >= 20 and npm >= 10 if adopting the action. Map existing repository secrets only inside the step that needs them:

```yaml
- name: Draft Zenodo Sandbox deposition with zenodraft
  uses: zenodraft/action@0.13.3
  env:
    ZENODO_SANDBOX_ACCESS_TOKEN: ${{ secrets.ZENODO_SANDBOX_TOKEN }}
  with:
    metadata: .zenodo.json
    sandbox: true
    publish: false
```

For production draft work, map `ZENODO_TOKEN` to `ZENODO_ACCESS_TOKEN` only in the zenodraft step. Keep production publish out of draft/archive workflows and retain the `zenodo-production-publish` protected environment for final publication.

## Sandbox proof

Zenodo Sandbox proof was completed on 2026-06-10 with a scoped
`deposit:write` token. The proof created an unsubmitted sandbox draft,
uploaded the generated metadata package files, updated draft metadata, and read
back the prereserved sandbox DOI. Non-secret proof details are recorded in
`manifests/zenodo_sandbox_proof.json`.

The proof draft remains unsubmitted and unpublished. It is not the canonical
dataset record and must not be cited as the production DOI-bearing release.

No production Zenodo publication evidence should be recorded until a reviewed draft is published through `zenodo-production-publish`.
