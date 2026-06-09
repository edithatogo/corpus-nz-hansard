# Spec: NZ Parliamentary Procedure Model

## MoSCoW Requirements

### Must

- Model party votes, personal votes, questions, supplementary questions, stages, rulings, interjections, and procedural units.
- Define how procedure components link to documents, sittings, members, parties, motions, bills, and votes.
- Record authority sources and uncertainty for each procedural category.

### Should

- Add fixtures for `Hansard - vote`, `Hansard - question`, and representative speech/procedure documents.
- Document mappings to ParlaMint, Popolo/Open Civic Data, Akoma Ntoso, and CAP/ParlaCAP.

### Could

- Add speech-act and debate-segment classifiers after gold/evaluation samples exist.

### Won't

- Treat all procedural text as speech turns.
- Infer validated voting records from surface text without procedural and authority validation.

## Acceptance Criteria

- Procedure component model, fixtures, and endpoint mapping notes exist.
