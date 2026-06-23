# Evidence: Wikipedia MP Lists

## Acquisition Results (2026-06-23)

### Script
`scripts/fetch_wikipedia_mps.py` fetches MP lists from Wikipedia for Parliaments 47-53 via the REST API (Parsoid HTML format).

The parser now supports both modern party-header tables and older per-row sortable wikitables, including Parsoid color-cell party metadata and escaped `party color` template attributes.

### Validation

`scripts/check_wikipedia_mp_lists_acquisition.py` validates:

- `derived/wikipedia_mp_lists.json` covers Parliaments 47-53 exactly.
- Each Parliament has the exact evidence-backed row count listed below.
- The regenerated artifact has exactly 895 MP references and internally consistent totals.
- The artifact records `source_articles` for every target Parliament, including REST URL, UTC fetch timestamp, fetch status, and `html_sha256` of the fetched Parsoid HTML.
- Party labels are restricted to known canonical labels.
- Conductor metadata and `conductor/tracks.md` list the track as complete or archived.

### Coverage

| Parliament | Article | MPs Extracted | Parties |
|---|---|---:|---|
| 47th | 47th_New_Zealand_Parliament | 122 | ACT, Green, Labour, National, NZ First, Progressive, United Future |
| 48th | 48th_New_Zealand_Parliament | 132 | ACT, Green, Labour, Maori Party, National, NZ First, Progressive, United Future |
| 49th | 49th_New_Zealand_Parliament | 132 | ACT, Green, Independent, Labour, Mana, Maori Party, National, Progressive, United Future |
| 50th | 50th_New_Zealand_Parliament | 132 | ACT, Green, Independent, Labour, Mana, Maori Party, National, NZ First, United Future |
| 51st | 51st_New_Zealand_Parliament | 128 | ACT, Green, Labour, Maori Party, National, NZ First, United Future |
| 52nd | 52nd_New_Zealand_Parliament | 125 | ACT, Green, Independent, Labour, National, NZ First |
| 53rd | 53rd_New_Zealand_Parliament | 124 | ACT, Green, Independent, Labour, National |

**Total: 895 MP records** across all 7 parliaments (47th-53rd).

### Known Notes

1. Resigned members are included when they served during the Parliament.
2. Party labels are normalized to canonical short labels for downstream joins.
3. The 54th Parliament remains covered by the curated current-Parliament source path rather than this historical acquisition script.
4. The track was archived after the 2026-06-23 review fixes because the focused checker and parser tests passed with the stricter provenance contract.

### Resolution Results (2026-06-12)

54th Parliament (curated): 41 names resolved with party/electorate
47th-53rd Parliaments (manual): 5 historical name variants resolved

- Brent Hudson -> Brett Hudson (National, 51st-52nd)
- Anahila Kanongata'a -> A. Kanongata'a-Suisuiki (Labour, 52nd-53rd)
- Asenati Lole-Taylor -> Asenati Taylor (NZ First, 50th)
- Gerrard Eckhoff -> Gerry Eckhoff (ACT, 47th-49th)
- Richard Posser -> Richard Prosser (NZ First, 50th-51st)

Total: 51 -> 50 resolved (98.0%), 1 remains (Laura Trask - non-MP)
