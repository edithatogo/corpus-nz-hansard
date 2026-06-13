#!/usr/bin/env python3
"""Create consolidated member registry from all identity sources."""

import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\60217257\OneDrive - Flinders\repos\corpus-nz-hansard'

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

print("Loading sources...")
final_res = load_json(f'{BASE}/derived/unmatched_final_resolution.json')
wikidata = load_json(f'{BASE}/derived/wikidata_nz_mps.json')
bills = load_json(f'{BASE}/derived/bills_api/bills_members_20260613T021002Z.json')
triang = load_json(f'{BASE}/derived/triangulated_member_authority.json')
parl_current = load_json(f'{BASE}/derived/parliament_current_mps.json')

# ── Build lookup indices ──────────────────────────────────────────────
wikidata_by_label = {}
wikidata_by_alias = {}
for rec in wikidata['member_records']:
    label = rec.get('label', '').lower()
    wikidata_by_label[label] = rec
    for alias in rec.get('aliases', []):
        wikidata_by_alias[alias.lower()] = rec

bills_set = set()
for name in bills['unique_members']:
    n = name
    for prefix in ['Hon ', 'Rt Hon ', 'Dr ', 'Sir ', 'Dame ', 'Mr ', 'Mrs ', 'Ms ', 'Miss ']:
        if n.startswith(prefix):
            n = n[len(prefix):]
    bills_set.add(n.lower().strip())

triang_by_name = {}
for rec in triang['member_records']:
    cn = rec.get('canonical_name', '').lower()
    triang_by_name[cn] = rec
    for alias in rec.get('aliases', []):
        triang_by_name[alias.lower()] = rec

parl_current_list = []
if isinstance(parl_current, dict) and 'members' in parl_current:
    parl_current_list = parl_current['members']
elif isinstance(parl_current, list):
    parl_current_list = parl_current
parl_by_name = {}
for mp in parl_current_list:
    if isinstance(mp, dict):
        n = mp.get('name', mp.get('full_name', '')).lower()
        if n:
            parl_by_name[n] = mp

# ── Helper ────────────────────────────────────────────────────────────
def normalize_party(p):
    if not p: return None
    pm = {
        'new zealand labour party': 'Labour',
        'new zealand national party': 'National',
        'new zealand first': 'NZ First',
        'act new zealand': 'ACT', 'act': 'ACT',
        'green party of aotearoa new zealand': 'Green',
        'green': 'Green',
        'te pati maori': 'Te Pati Maori',
        'te pāti māori': 'Te Pati Maori',
        'maori party': 'Te Pati Maori',
        'united future': 'United Future',
        'national': 'National',
        'labour': 'Labour',
        'nz first': 'NZ First',
    }
    return pm.get(p.lower().strip(), p)

def lookup_wikidata(name_lower):
    if name_lower in wikidata_by_label:
        return wikidata_by_label[name_lower]
    if name_lower in wikidata_by_alias:
        return wikidata_by_alias[name_lower]
    return None

def in_bills(name_lower):
    return name_lower in bills_set

# ── Build consolidated registry ───────────────────────────────────────
registry = {}

for hansard_name, info in final_res['results'].items():
    entry = {
        'hansard_name': hansard_name,
        'canonical_name': info.get('matched_name') or info.get('wiki_name') or hansard_name,
        'party': normalize_party(info.get('party', '')),
        'parliament_numbers': [],
        'sources_used': [],
        'confidence': 'high',
        'resolved': info.get('resolved', False),
    }
    
    if info.get('resolved'):
        entry['sources_used'].append(info.get('source', 'unknown'))
        canonical_lower = entry['canonical_name'].lower()
        
        if in_bills(canonical_lower):
            entry['sources_used'].append('Bills API')
        
        wd = lookup_wikidata(canonical_lower)
        if wd:
            entry['sources_used'].append('Wikidata SPARQL')
            pl = wd.get('parliament_label', '')
            if pl:
                nums = re.findall(r'(\d+)(?:st|nd|rd|th)', pl)
                entry['parliament_numbers'] = [int(n) for n in nums]
            if not entry.get('party') and wd.get('party'):
                entry['party'] = normalize_party(wd['party'])
        
        tn = triang_by_name.get(canonical_lower)
        if tn:
            entry['sources_used'].append('Triangulated Authority')
        
        for pname, pmp in parl_by_name.items():
            if canonical_lower in pname or pname in canonical_lower:
                entry['sources_used'].append('Parliament Current')
                if not entry.get('party') and pmp.get('party'):
                    entry['party'] = normalize_party(pmp['party'])
                break
        
        if 'notes' in info:
            entry['notes'] = info['notes']
        if 'electorate' in info:
            entry['electorate'] = info['electorate']
        
        entry['confidence'] = 'high' if len(entry['sources_used']) >= 2 else 'medium'
    else:
        entry['confidence'] = 'low'
        entry['notes'] = info.get('notes', '')
    
    registry[hansard_name] = entry

# ── Laura Trask: resolved via Bills API ───────────────────────────────
if 'Laura Trask' in registry:
    lt = registry['Laura Trask']
    lt['canonical_name'] = 'Laura McClure'
    lt['party'] = 'ACT'
    lt['resolved'] = True
    lt['sources_used'] = ['Bills API', 'Hansard Context (54th Parl, ACT colleagues)']
    lt['confidence'] = 'medium'
    lt['notes'] = 'Laura Trask mapped to Laura McClure (ACT MP). Bills API lists Laura McClure, not Laura Trask. Hansard shows her in 54th Parl (2024) alongside ACT MPs David Seymour, Simon Court, Karen Chhour, Brooke van Velden.'
    lt['parliament_numbers'] = [54]

# ── Summary ───────────────────────────────────────────────────────────
total = len(registry)
resolved = sum(1 for v in registry.values() if v.get('resolved'))
unresolved = total - resolved
rate = round(resolved / total * 100, 1) if total else 0

registry_meta = {
    "total_members": total,
    "resolved": resolved,
    "unresolved": unresolved,
    "resolution_rate_pct": rate,
    "generated_at": "2026-06-13",
    "sources_integrated": [
        "unmatched_final_resolution.json (50/51 resolved)",
        "wikidata_nz_mps.json (1,514 records)",
        "bills_members API (351 unique members)",
        "triangulated_member_authority.json",
        "parliament_current_mps.json",
        "Hansard corpus (193,922 rows)"
    ],
    "members": registry
}

outpath = f'{BASE}/derived/member_registry.json'
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(registry_meta, f, indent=2, ensure_ascii=False)

print(f"Written {outpath}")
print(f"Total: {total}, Resolved: {resolved}, Unresolved: {unresolved}, Rate: {rate}%")
for name, e in registry.items():
    s = '+' if e.get('resolved') else '-'
    print(f"  {s} {name:45s} -> {e['canonical_name']:30s} [{e.get('party','?') or '?'}] conf={e['confidence']}")

