# Evidence: Wikipedia MP Lists

## Acquisition Results (2026-06-13)

### Script
`scripts/fetch_wikipedia_mps.py` — fetches MP lists from Wikipedia for Parliaments 47-53 via the REST API (Parsoid HTML format).

### Coverage

| Parliament | Article | MPs Extracted | Notes |
|---|---|---|---|
| 47th | 47th_New_Zealand_Parliament | 0 | Uses older wikitable format — not yet supported |
| 48th | 48th_New_Zealand_Parliament | 0 | Same format as 47th |
| 49th | 49th_New_Zealand_Parliament | 0 | Same format as 47th |
| 50th | 50th_New_Zealand_Parliament | 0 | Same format as 47th |
| 51st | 51st_New_Zealand_Parliament | 0 | Same format as 47th |
| 52nd | 52nd_New_Zealand_Parliament | 125 | Modern table format — parsed correctly |
| 53rd | 53rd_New_Zealand_Parliament | 124 | Modern table format — parsed correctly |

**Total: 249 MP records** across 2 parliaments (52nd-53rd).

### Party Breakdown

**52nd Parliament (125 MPs):**
- National: 60 (includes resigned members)
- Labour: 46
- NZ First: 9
- Green: 8
- ACT: 1
- Independent: 1 (Jami-Lee Ross)

**53rd Parliament (124 MPs):**
- Labour: 66 (includes resigned members)
- National: 36
- ACT: 10
- Green: 9
- Independent: 3

### Known Limitations

1. **Parliaments 47-51**: These use an older sortable wikitable format where party names appear in `<td>` cells (2nd column) rather than `<th>` headers. The current parser targets the modern format where party sections use `<th>` headers like "Labour (62)". A separate extraction strategy is needed for these older parliaments.

2. **Resigned members**: The extracted counts include MPs who resigned during the term (e.g., Jacinda Ardern, Trevor Mallard in 53rd; Bill English, Steven Joyce in 52nd). These are valid MPs who served during the parliament.

3. **Electorate extraction**: Some electorates may include minor formatting artifacts due to the HTML parsing approach.

### Resolution Results (2026-06-12)

54th Parliament (curated): 41 names resolved with party/electorate
47th-53rd Parliaments (manual): 5 historical name variants resolved
- Brent Hudson -> Brett Hudson (National, 51st-52nd)
- Anahila Kanongata'a -> A. Kanongata'a-Suisuiki (Labour, 52nd-53rd)
- Asenati Lole-Taylor -> Asenati Taylor (NZ First, 50th)
- Gerrard Eckhoff -> Gerry Eckhoff (ACT, 47th-49th)
- Richard Posser -> Richard Prosser (NZ First, 50th-51st)

Total: 51 -> 50 resolved (98.0%), 1 remains (Laura Trask - non-MP)
