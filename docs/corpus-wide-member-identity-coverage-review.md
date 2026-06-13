# Corpus-Wide Member Identity Authority — Coverage Review

**Track ID:** `corpus_wide_member_identity_release_20260610`  
**Review Date:** 2026-06-12  
**Reviewer:** Authority Coverage Auditor (auto-generated)  
**Status:** ⛔ BLOCKED — coverage gaps identified

---

## 1. Overview

The auto-derived member identity authority (`derived/corpus_wide_member_identity_authority.json`) was analysed for coverage quality, data integrity, and alignment with official NZ Parliament sources documented in `manifests/authority_sources.json`.

| Metric | Value |
|---|---|
| Records in authority file | **408** |
| Records claimed in task brief | 4,505 (⚠️ see §2.1) |
| Official member-domain sources | 5 (3 authoritative + 2 supporting) |
| Release gate | `blocked-pending-authority-coverage-review` |

---

## 2. Record Count Discrepancy

### 2.1 Count Mismatch

The task brief states **4,505 auto-derived records**, but the actual `member_records` array contains **exactly 408 entries** — a ~90% discrepancy.

Possible explanations:
- The brief figure may include a different revision of the authority file.
- The count may conflate row-level identity resolution records (member_identity.csv) with the deduplicated authority.
- The brief figure may be from a pre-deduplication stage.

**Recommendation:** Clarify the expected record count before gate advancement.

---

## 3. Data Completeness Issues

### 3.1 Missing Authority URLs

| Status | Count |
|---|---|
| Empty `authority_url` | **408 / 408 (100%)** |
| Populated `authority_url` | 0 |

No record links to an official NZ Parliament member page, former member page, or roll-of-members PDF.

### 3.2 Missing Service Periods

| Status | Count |
|---|---|
| Empty `service_periods` | **408 / 408 (100%)** |
| Populated `service_periods` | 0 |

The authority file explicitly notes these are intentionally unpopulated.

### 3.3 Missing Aliases

| Status | Count |
|---|---|
| Records **with** aliases | **2 / 408 (0.5%)** |
| Records **without** aliases | **406 / 408 (99.5%)** |

Only 2 records have any aliases. This is extremely low for a corpus spanning decades where name variants are common.

---

## 4. Data Quality Issues

### 4.1 Non-Person Entries (3 records)

Procedural roles or fragments, not actual MPs — should be removed:

| canonical_name | Issue |
|---|---|
| `Presiding Officer` | Procedural role, not a person |
| `The Clerk` | Procedural role, not a person |
| `Ang` | Truncated/fragment name; not a valid MP |

### 4.2 Reversed Name Order (1 record)

| canonical_name | Issue |
|---|---|
| `Foster-Bell Paul` | Surname-first — should be `Paul Foster-Bell` (which exists separately) |

This is a de facto duplicate entry.

### 4.3 Honorific Embedded in Canonical Name (1 record)

| canonical_name | Issue |
|---|---|
| `Hon Aupito William Sio` | `Hon` prefix should have been stripped per derivation rules |

Also has near-duplicate variants (see §4.4).

### 4.4 Near-Duplicate Groups

Likely the same person under different name forms — need human review:

| Group | Records |
|---|---|
| **William Sio** (3 records) | `William Sio`, `Su'a William Sio`, `Hon Aupito William Sio` |
| **Anahila Kanongata'a** (2) | `Anahila Kanongata'a`, `Anahila Kanongata'a-Suisuiki` |
| **Jo Hayes** (2) | `Jo Hayes`, `Joanne Hayes` |
| **Hilary Calvert** (2) | `Hilary Calvert`, `Hilary Jane Calvert` |
| **Russel Norman** (2) | `Russel Norman`, `Russel William Norman` |
| **Peseta/Sam Lotu-Iiga** (2) | `Peseta Sam Lotu-Iiga`, `Sam Lotu-Iiga` |
| **Tāmati/Tamati Coffey** (2) | `Tamati Coffey`, `Tāmati Coffey` — **confirmed duplicate** |
| **Brett/Brent Hudson** (2) | `Brett Hudson`, `Brent Hudson` — requires verification |

**Total individuals affected:** ~12–15

### 4.5 Initials in Name (1 record)

`H V Ross Robertson` — initials `H V` appear before the given name (non-standard format).

---

## 5. Comparison Against Official Sources

### 5.1 Official Member-Domain Sources

Per `manifests/authority_sources.json`, the member domain has these primary sources:

| Source ID | Classification | Coverage |
|---|---|---|
| `nz-parliament-members-current` | **Authoritative** | Current 54th Parliament (123 MPs) |
| `nz-parliament-former-members` | **Authoritative** | Historical former-member register |
| `nz-parliament-roll-of-members` | **Authoritative** | Historical roll from 1854 onwards |
| `nz-parliament-member-contact-downloads` | Supporting | Current contact details |
| `electoral-commission-election-results` | Supporting | Election/candidate context |

### 5.2 Validation Status

| Requirement | Status |
|---|---|
| Cross-referenced against current members page | ❌ Not done |
| Cross-referenced against former members page | ❌ Not done |
| Cross-referenced against roll-of-members PDF | ❌ Not done |
| Service periods verified | ❌ Not done |
| Official member IDs assigned | ❌ Not done |
| Name variants/aliases populated | ⚠️ Minimal (0.5%) |
| Non-person entries removed | ❌ 3 remain |

### 5.3 Coverage Gaps

1. **No authority URLs** — every record lacks links to Parliament sources.
2. **No service periods** — cannot verify MP tenure.
3. **No external member IDs** — no alignment with Parliament identifiers.
4. **Undocumented name variants** — 99.5% lack aliases.
5. **Possible missing members** — 408 records is far fewer than the ~1,000+ MPs since 1854.

---

## 6. Statistical Summary

| Category | Count | % of Total |
|---|---|---|
| Total records | 408 | 100% |
| Valid-looking MP records | ~388 | ~95% |
| Non-person entries (remove) | 3 | 0.7% |
| Honorific in canonical name | 1 | 0.2% |
| Reversed name order | 1 | 0.2% |
| Initials in name | 1 | 0.2% |
| Records with aliases | 2 | 0.5% |
| Near-duplicate groups | ~10 groups | ~6% |
| Macron/Unicode variants | 1 pair | 0.5% |
| Empty authority_url | 408 | 100% |
| Empty service_periods | 408 | 100% |

---

## 7. Action Items

### 7.1 Must-Fix Before Release

1. **Remove non-person entries:** `Presiding Officer`, `The Clerk`, `Ang`
2. **Merge reversed name:** `Foster-Bell Paul` → consolidate with `Paul Foster-Bell`
3. **Strip honorific:** `Hon Aupito William Sio` → investigate merge with `William Sio` / `Su'a William Sio`
4. **Merge confirmed duplicate:** `Tamati Coffey` ↔ `Tāmati Coffey`
5. **Populate authority URLs:** Link every record to official Parliament pages

### 7.2 Should-Fix Before Release

6. **Review near-duplicate groups** (§4.4) and consolidate where same person
7. **Verify Brett Hudson vs Brent Hudson** — different people or error?
8. **Resolve `H V Ross Robertson`** to consistent format
9. **Expand alias population** for the 406 records currently without aliases
10. **Verify `Dr Anae Neru Leavasa`** alias handling

### 7.3 Future Enhancement

11. **Service period resolution** from roll-of-members PDF and former members page
12. **External member ID alignment** with official Parliament identifiers
13. **Historical completeness assessment** against full roll of members

---

## 8. Recommendations

1. **Confirm the record count** — investigate why brief states 4,505 but file has 408.
2. **Re-run alias extraction** — the current pipeline produced only 2 alias records.
3. **Block release** until all Must-Fix items are resolved.
4. **Schedule a human review pass** over near-duplicate groups for consolidation decisions.
5. **After fixes, re-run builder** and produce a fresh coverage review before gate advancement.

---

## 9. Appendix: Resolution Rules Assessment

The authority file states these derivation rules:
- Honorifics (Hon, Rt Hon, Dr, Sir, Dame, Mr, Mrs, Ms, Miss, Prof) are stripped before normalisation.
- Semicolon-delimited raw values are split into separate tokens.
- Most common variant becomes canonical; less-common variants become aliases.
- Service periods, official IDs, and authority URLs are intentionally unpopulated.

**Rule violations found:**
- `Hon Aupito William Sio` retains `Hon` in canonical name (rule: strip honorifics).
- Only 2 of 408 records have aliases despite likely many corpus name variants (rule: less-common variants become aliases).
- `Foster-Bell Paul` entered canonical form in reversed order.
