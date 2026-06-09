# Spec: Historical Coverage Audit

## MoSCoW Requirements

### Must

- Define coverage claims separately for supplied archive completeness and historical Hansard completeness.
- Compare available source files, parliaments, dates, document types, rows, and known gaps.
- Record uncertainty explicitly in release and endpoint documentation.

### Should

- Cross-check against official parliamentary period and sitting metadata when authority sources exist.
- Produce a coverage manifest and human-readable report.

### Could

- Add gap visualizations by parliament, date, and document type.

### Won't

- Claim full historical coverage solely from the supplied source archive.

## Acceptance Criteria

- Coverage manifest and report distinguish verified, partial, unknown, and excluded historical ranges.
