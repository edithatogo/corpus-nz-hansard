# Spec: Popolo / Open Civic Data Endpoint

## MoSCoW Requirements

### Must

- Generate people, organizations, memberships, motions, vote events, votes, and speech references where validated inputs exist.
- Validate date ranges and referential integrity.
- Distinguish party votes from individual votes.
- Preserve provenance for every civic-data object.

### Should

- Align fields with Popolo and Open Civic Data conventions.
- Add JSONL outputs for large corpus use.
- Include examples for mySociety/PublicWhip-style parser comparison.

### Could

- Add RDF output after the RDF endpoint exists.

### Won't

- Infer full voting records from text patterns alone.
- Submit NZ data to UK-focused upstream projects without maintainer agreement.

## Acceptance Criteria

- Civic-data artifacts validate locally and include source provenance.
- Vote artifacts have explicit motion/procedural-question linkage or are marked incomplete.

## Dependencies

- Depends on authority-source discovery, canonical ID/URI policy, member identity, party attribution, NZ parliamentary procedure model, vote/motion extraction, and release ladder.
