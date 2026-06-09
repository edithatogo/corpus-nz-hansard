# Spec: Akoma Ntoso Endpoint

## MoSCoW Requirements

### Must

- Select and document the Akoma Ntoso profile or subset used.
- Preserve source order and provenance in generated XML.
- Validate XML well-formedness and available schema constraints.

### Should

- Cover bills, motions, votes, questions, and proceeding items.
- Add NZ-specific mapping notes.

### Could

- Generate fragments first, then full sitting documents after proceeding segmentation matures.

### Won't

- Claim complete legislative-document modeling before bill and vote authority sources are validated.

## Acceptance Criteria

- Sample Akoma Ntoso output, mapping notes, and validation manifest exist.

## Dependencies

- Depends on neutral proceeding components, authority-source discovery, canonical ID/URI policy, NZ parliamentary procedure model, bills, motions, votes, questions, and release ladder.
