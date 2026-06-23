# Track: Member Identity Triangulation

Combine multiple sources to resolve Hansard member names.

## Sources
1. Wikipedia 54th Parliament (curated) - 41 resolved
2. Wikipedia 47th-53rd Parliaments - 5 resolved
3. Wikidata SPARQL (1,514 records) - 4 resolved
4. Bills API member sponsors - integrated (1 additional resolution plus cross-checks)
5. HathiTrust historical volumes - blocked/not required for the 51/51 result
6. Parliament website and Electoral Commission sources - deferred to future authority enrichment tracks

## Results
- Total: 51 unmatched names
- Resolved: 51 (100.0%)
- Remaining: 0
- Final additional mapping: Laura Trask -> Laura McClure (ACT), medium confidence via Bills API and Hansard context
- Consolidated output: `derived/member_registry.json`
- Checker: `scripts/check_member_identity_triangulation.py`
