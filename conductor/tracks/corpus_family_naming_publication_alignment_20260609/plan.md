# Plan: Corpus Family Naming And Publication Alignment

## Phase 1: Naming and documentation

- [ ] Task 1.1: Record `corpus-nz-hansard` and `corpus-nz-legislation` as preferred family labels in Conductor product/setup docs.
- [ ] Task 1.2: Update MoSCoW requirements with cross-corpus publication-surface requirements.
- [ ] Task 1.3: Update interoperability design with cross-corpus Mermaid diagrams and environment gates.
- [ ] Task 1.4: Update hosting decision matrix with GitHub/HF/Zenodo/OSF/future metadata responsibilities.

## Phase 2: GitHub environment

- [ ] Task 2.1: Audit GitHub description, homepage, topics, license, releases, Actions, branch protections, CodeQL, Scorecard, Renovate, README, and sibling links.
- [ ] Task 2.2: Align release naming and docs with `corpus-nz-hansard` and sibling `corpus-nz-legislation` references.
- [ ] Task 2.3: Record migration/non-migration decisions for public names.

## Phase 3: Hugging Face environment

- [ ] Task 3.1: Audit dataset card front matter, file layout, Xet status, DOI/GitHub links, access/gating, and viewer health.
- [ ] Task 3.2: Verify whether any public viewer split/cast or file-layout issue exists, then fix confirmed issues with evidence.
- [ ] Task 3.3: Add sibling corpus links and record HF revision/access evidence.

## Phase 4: Zenodo environment

- [ ] Task 4.1: Audit canonical and superseded Zenodo records, files, license metadata, related identifiers, and version chain.
- [ ] Task 4.2: Align Zenodo metadata with GitHub/Hugging Face and source-rights caveats.
- [ ] Task 4.3: Document DOI update rules for dataset card, CITATION, and release notes.

## Phase 5: OSF and other environments

- [ ] Task 5.1: Decide whether OSF is needed for review bundles or mirrors.
- [ ] Task 5.2: If OSF is used, define file-size/splitting, checksum, citation, and update cadence policy.
- [ ] Task 5.3: Add generated metadata roadmap tasks for Croissant, RO-Crate, Frictionless, DCAT, and PROV-O.

## Final Verification

- [ ] All environment tasks are present.
- [ ] Requirements/design/hosting docs are updated.
- [ ] Conductor tracks registry includes this track.
- [ ] Evidence records current public-surface audit results.
