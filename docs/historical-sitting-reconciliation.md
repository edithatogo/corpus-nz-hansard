# Historical Sitting Reconciliation

This document defines the comparison contract for reconciling the supplied
DocumentsDB Hansard extract against official parliamentary sitting and
proceeding surfaces.

The official export path currently recorded for execution is the PDF journal
export surface documented in `docs/historical-sitting-official-exports.md`, not
the HTML archive pages that trigger challenge responses in automation.

## Scope

- Compare the normalized corpus holdings against the official sitting inventory.
- Use the official source surfaces for sitting-day, week-level, and archival
  reconciliation.
- Keep completeness claims blocked until the comparison is actually run.
- Prepare the comparison ledger as a separate normalized artifact before any
  official comparison result is claimed.

## Official Sources

- Parliamentary Business
- Historic Journals of the House
- Daily progress in the House
- Indexes to the Journals
- Order Paper
- Weekly Journals Archive
- Sessional Journals archive
- Hansard

## Comparison Contract

The comparison keys are normalized publication titles, sitting dates,
parliament numbers, source stable IDs, publication surfaces, issue or volume
references, and entry sequence values.

The comparison keys are intentionally conservative so a row by row pass can be
run without guessing at publication identity.

The tolerance rules are intentionally conservative:

- normalize whitespace, punctuation, and title casing before comparison
- allow same-day publication lag between provisional and final parliamentary
  pages
- compare journal archives at week or sessional scope rather than by web page
  presentation
- compare historic journals at year, volume, and page scope when present
- treat Hansard as the canonical text record for debate-level reconciliation
- classify sources missing from the official inventory as unavailable

## Gap Taxonomy

The gap taxonomy is:

- missing
- duplicate
- partial
- malformed
- unavailable
- inconsistent
- out_of_scope

The reconciliation output must classify gaps with that taxonomy.

That gap taxonomy must support a missing, duplicate, partial, malformed, and
unavailable classification pass before any completeness claim is made.

## Boundary

This is a contract document, not the reconciliation result itself. The actual
comparison still has to be run against the corpus holdings before the track can
be marked complete. The repository is now comparison-ready, but the official
comparison outcome is not yet published.
