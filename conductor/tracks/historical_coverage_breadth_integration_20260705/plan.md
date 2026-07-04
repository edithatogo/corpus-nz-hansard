# Historical Coverage Breadth Integration Plan

## Phase 1: Define the Cross-Repo Coverage Model

- [ ] Task: Draft the family-level historical coverage taxonomy for official, fallback, supporting, excluded, and evidence-only sources.
- [ ] Task: Define the reconciliation manifest shape for historical gaps, source posture, and adjacent-repo evidence pointers.
- [ ] Task: Specify the cross-repo boundary rules for `hathi-nz` and `corpus-law-nz`.
- [ ] Task: Conductor - User Manual Verification 'Define the Cross-Repo Coverage Model' (Protocol in workflow.md)

## Phase 2: Implement the Manifest and Validation Surface

- [ ] Task: Create the reconciliation manifest builder and schema for the coverage ledger.
- [ ] Task: Add docs that explain how historical completeness is inferred from the ledger without making completeness claims.
- [ ] Task: Add checker coverage for source classification, excluded-source handling, and fallback promotion guardrails.
- [ ] Task: Add unit tests for manifest validation and boundary classification.
- [ ] Task: Conductor - User Manual Verification 'Implement the Manifest and Validation Surface' (Protocol in workflow.md)

## Phase 3: Integrate Adjacent Repos and Validate

- [ ] Task: Add cross-repo references that point to the HathiTrust-side Hansard evidence and the legislation boundary docs.
- [ ] Task: Run the repo validation gates and verify the cross-repo references stay evidence-only where required.
- [ ] Task: Update track evidence with the final manifest, checker results, and repository-boundary summary.
- [ ] Task: Conductor - User Manual Verification 'Integrate Adjacent Repos and Validate' (Protocol in workflow.md)
