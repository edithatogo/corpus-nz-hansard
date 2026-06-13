import json
import unicodedata
from pathlib import Path

auth = json.load(open(Path.home() / "OneDrive - Flinders" / "repos" / "corpus-nz-hansard" / "derived" / "corpus_wide_member_identity_authority.json", encoding="utf-8"))
unmatched = [r for r in auth["member_records"] if r.get("resolution_scope", "") == "corpus-auto-derived-unmatched"]
names = [r["canonical_name"] for r in unmatched]

wiki = json.loads(Path("_wiki_nz_mps.json").read_text(encoding="utf-8"))

def nfkd(v):
    nf = unicodedata.normalize("NFKD", v)
    return "".join(c for c in nf if unicodedata.category(c) != "Mn")

def norm(n):
    # Simple normalization without importing _normalize_token
    value = " ".join(n.replace(".", "").split())
    prefixes = ("RT HON ", "HON ", "DR ", "SIR ", "DAME ", "MR ", "MRS ", "MS ", "MISS ", "PROF ")
    upper = value.upper()
    for prefix in prefixes:
        if upper.startswith(prefix):
            value = value[len(prefix):].strip()
            break
    return nfkd(value.upper().strip())

matched = 0
for n in sorted(names):
    n_norm = norm(n)
    found = []
    for w in wiki:
        w_clean = w.split("(")[0].strip() if "(" in w else w
        if n_norm == norm(w_clean) or n_norm == norm(w):
            found.append(w)
            break
    if found:
        matched += 1
        print(f"  WIKI: {n[:32]:32s} -> {found[0]}")
    else:
        print(f"  MISS: {n[:32]:32s}")

print(f"\nMatched: {matched}/{len(names)} ({matched*100//len(names)}%)")
