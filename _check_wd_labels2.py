import json
wd = json.load(open("derived/wikidata_nz_mps.json", encoding="utf-8"))
labels = [r.get("label","") for r in wd["member_records"]]
names = ["Cameron Brewer","Celia Wade-Brown","Darleen Tana","Hana-Rawhiti Maipi-Clarke","Nancy Lu","Todd Stephenson","Andy Foster","Anae Neru Leavasa","Peseta Sam Lotu-Iiga","Paul Tamatha","H V Ross Robertson","R Doug Woolerton"]
for n in names:
    found = [l for l in labels if n.lower() in l.lower()]
    print(f"{n:35s} | {len(found)} matches | {found[:1]}")
# Also check with nfkd normalization
import unicodedata
def nfkd(v):
    nf = unicodedata.normalize("NFKD", v)
    return "".join(c for c in nf if unicodedata.category(c) != "Mn")
macron_names = ["H\u0101hana Lyndon", "T\u0101kuta Ferris"]
for n in macron_names:
    found = [l for l in labels if nfkd(n).lower() in nfkd(l).lower()]
    print(f"{n:35s} | {len(found)} matches | {found[:1]}")
    # Also try searching without the macron-nfkd version
    plain = nfkd(n)
    found2 = [l for l in labels if plain.lower() in l.lower()]
    print(f"{plain:35s} | {len(found2)} matches | {found2[:1]}")
