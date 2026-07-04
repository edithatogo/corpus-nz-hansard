# Historical Coverage Breadth Integration

Release posture: evidence-only.

This bridge manifest makes a no completeness claim. It links the Parliament website inventory to adjacent historical evidence sources without claiming completeness. It keeps NZ legislation and the Gazette out of scope, and it treats HathiTrust and other historical resources as gap-detection evidence and discovery evidence while preserving the distinction between discovery evidence and acquisition evidence.

## Coverage model

- Official: Parliament website sources that remain the anchor.
- Fallback: Papers Past, Google Books, and library catalogues used only to narrow historical gaps.
- Supporting: Contextual sources such as O Nehera for British Parliamentary Papers relationships.
- Evidence-only: Data.govt.nz requests and similar demand signals.
- Excluded: NZ legislation and Gazette, plus other non-primary baselines.

## Adjacent repos

- `hathi-nz` supplies HathiTrust-side Hansard discovery and archive evidence.
- `corpus-law-nz` remains the legislation/Gazette boundary reference.

## Guardrails

- Do not claim full historical completeness.
- Do not promote fallback sources to official sources without manifest changes.
- Do not use this bridge as a bulk-acquisition dependency.
