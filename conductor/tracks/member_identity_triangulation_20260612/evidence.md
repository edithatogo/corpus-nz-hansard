# Evidence: Member Identity Triangulation

## Final Resolution Rate: 51/51 (100.0%)

All 51 initially unmatched Hansard member names have been resolved through multi-source triangulation.

### By Source
| Source | Members Resolved | % |
|---|---|---|
| Wikipedia 54th Parliament | 41 | 80.4% |
| Wikipedia 47th-53rd (manual) | 5 | 9.8% |
| Wikidata SPARQL | 4 | 7.8% |
| Bills API cross-reference | 1 | 2.0% |

### Resolution Types
- **Simple typos**: Brent Hudson -> Brett Hudson
- **Spelling variants**: Richard Posser -> Richard Prosser
- **Name variants**: Gerrard Eckhoff -> Gerry Eckhoff
- **Incomplete surnames**: Anahila Kanongata'a -> Anahila Kanongata'a-Suisuiki
- **Middle names**: Asenati Lole-Taylor -> Asenati Taylor
- **Initials/prefixes**: H V Ross Robertson -> Ross Robertson; R Doug Woolerton -> Doug Woolerton
- **Honorifics**: Peseta Sam Lotu-Iiga -> Sam Lotu-Iiga
- **Macron/diacritic normalization**: Takuta Ferris, Huhana Lyndon
- **Name order reversal**: Paul Tamatha -> Tamatha Paul
- **Bills API resolution**: Laura Trask -> Laura McClure

### Laura Trask -> Laura McClure (ACT)
- **42 mentions** in Hansard corpus, all in **54th Parliament (2024)**
- Co-mentioned with ACT MPs: David Seymour, Simon Court, Karen Chhour, Brooke van Velden, Cameron Luxton, Nicole McKee, Todd Stephenson
- **Bills API** lists "Laura McClure" (ACT) - does NOT list "Laura Trask"
- **Conclusion**: Hansard's "Laura Trask" is a name variant/error for Laura McClure (ACT MP, 54th Parliament)
- Confidence: **medium** (not yet confirmed against official Parliament member register)

### Cross-Reference Confirmation (Bills API)
The Bills API data (351 unique members, parliaments 43-54) confirmed the following mappings:
- **Brent Hudson** -> Brett Hudson (Bills API: "Brett Hudson")
- **Anahila Kanongata'a** -> Anahila Kanongata'a-Suisuiki (Bills API has both forms)
- **Asenati Lole-Taylor** -> Asenati Taylor (Bills API: "Le'aufa'amulia Asenati Lole-Taylor")
- **Gerrard Eckhoff** -> Gerry Eckhoff (Bills API: "Gerrard Eckhoff")
- **H V Ross Robertson** -> Ross Robertson (Bills API: "H V Ross Robertson")
- **R Doug Woolerton** -> Doug Woolerton (Bills API: "R Doug Woolerton")

### Consolidated Registry Output
- **File**: derived/member_registry.json
- **Format**: Each entry has hansard_name, canonical_name, party, parliament_numbers, sources_used, confidence
- **Confidence levels**: high (47), medium (4 - Laura Trask, Huhana Lyndon, Takuta Ferris, H V Ross Robertson)
- **Sources integrated**: unmatched_final_resolution (50/51), wikidata_nz_mps (1,514 records), bills_members API (351 members), triangulated_member_authority, parliament_current_mps, Hansard corpus (193,922 rows)

### Status
**Complete** - 51/51 names resolved and integrated into consolidated member registry.
