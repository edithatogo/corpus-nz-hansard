# Evidence

Release posture: evidence-only.

Evidence added:

- `scripts/build_historical_coverage_breadth_integration.py` generates the bridge manifest and docs.
- `scripts/check_historical_coverage_breadth_integration.py` validates schema, posture, boundary rules, and adjacent-repo references.
- `tests/test_historical_coverage_breadth_integration.py` exercises build and validation.
- `manifests/historical_coverage_breadth_integration.json` records the cross-repo coverage model.
- The bridge makes a no completeness claim.
- The coverage posture uses gap-detection evidence and discovery evidence instead of bulk-acquisition claims.
- HathiTrust remains a historical Hansard evidence companion, not a completeness source.

## Repository boundary summary

- `corpus-nz-hansard` remains the Parliament website anchor.
- `hathi-nz` is cited only for historical Hansard discovery and archive evidence.
- `corpus-law-nz` remains the legislation/Gazette boundary reference.

This bridge does not claim historical completeness or bulk-acquisition readiness.
