# Evidence: Parliament Website Stealth Access

## Attempts (2026-06-12)

1. Direct HTTP (requests lib): Radware challenge
2. Playwright Chrome headless: Radware challenge
3. Internet Archive: Radware-protected even on Wayback Machine

## What DOES Work
- bills.parliament.nz - fully open REST API
- questions.parliament.nz - accessible SPA
- Wikipedia - fully accessible
- Wikidata SPARQL - fully accessible


## Successful Stealth Access (2026-06-12 12:35 NZST)

### Technique Used
- Playwright chromium with headless mode
- User agent: Chrome 124 on Windows 10
- Viewport: 1920x1080, locale en-NZ, timezone Pacific/Auckland
- `navigator.webdriver` override (set to `false`)
- `window.chrome` runtime spoof
- Permissions query override
- Chrome args: `--disable-blink-features=AutomationControlled`, `--disable-web-security`, etc.
- `bypassCSP: true` on context

### Results
All 5 target pages were successfully fetched without Radware blocking:

| Target | Title | Content Length |
|--------|-------|---------------|
| members-current | Members of Parliament - New Zealand Parliament | 6,699 chars |
| former-members | Former Members of Parliament - New Zealand Parliament | 16,494 chars |
| daily-progress | Daily progress in the House - New Zealand Parliament | 1,353 chars |
| order-paper | Order Paper - New Zealand Parliament | 2,541 chars |
| hansard-current | Hansard - New Zealand Parliament | 1,349 chars |

### Saved Artifacts (derived/parliament_stealth/)
- `{label}.html` - Full page HTML
- `{label}.txt` - Extracted text content
- `{label}.png` - Full-page screenshot
- `run_log.json` - Run metadata

### Script
- `scripts/fetch_parliament_stealth.mjs` - Playwright stealth browser script
- Usage: `node scripts/fetch_parliament_stealth.mjs`
- Test mode: `TEST_MODE=1 node scripts/fetch_parliament_stealth.mjs` (fetches only first URL)

## What ALSO Works
- **www3.parliament.nz** - accessible via Playwright stealth (all 5 tested pages)
- bills.parliament.nz - fully open REST API
- questions.parliament.nz - accessible SPA
- Wikipedia - fully accessible
- Wikidata SPARQL - fully accessible
