# Spec: Authority Source Discovery

## MoSCoW Requirements

### Must

- Identify candidate official sources for members, parties, offices, sittings, bills, motions, votes, and procedure.
- Record source URL, publisher, retrieval date, source hash, coverage period, licence/reuse note, and access constraints.
- Classify each source as authoritative, supporting, candidate, or rejected.
- Create a manifest format for authority-source inventories.

### Should

- Include official New Zealand Parliament sources first.
- Include fallback civic or archival sources only when official sources are unavailable or incomplete.
- Record source refresh cadence and historical coverage gaps.

### Could

- Add automated source retrieval where licence and access conditions permit.

### Won't

- Treat text-derived inference as an authority source.
- Publish authoritative member, party, bill, vote, or sitting fields without declared authority inputs.

## Acceptance Criteria

- Authority-source manifest exists with at least candidate coverage for all target domains.
- Downstream tracks can cite authority source IDs and coverage notes.
