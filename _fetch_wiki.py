from pathlib import Path
import json
import requests

titles = set()
cmcontinue = ""
n = 0
print("Fetching Wikipedia category members...")
api = "https://en.wikipedia.org/w/api.php"

while True:
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Category:Members_of_the_New_Zealand_House_of_Representatives",
        "cmlimit": "max",
        "format": "json",
    }
    if cmcontinue:
        params["cmcontinue"] = cmcontinue
    
    r = requests.get(api, params=params, headers={"User-Agent": "corpus-nz/1.0"}, timeout=120)
    d = r.json()
    for p in d["query"]["categorymembers"]:
        titles.add(p["title"])
    n += len(d["query"]["categorymembers"])
    print(f"  {n} fetched...")
    
    cmcontinue = d.get("continue", {}).get("cmcontinue", "")
    if not cmcontinue:
        break

Path("_wiki_nz_mps.json").write_text(json.dumps(sorted(titles)), encoding="utf-8")
print(f"Done: {len(titles)} total")
