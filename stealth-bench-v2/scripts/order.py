"""Recovers Browser Use's site-by-site column order from their page grid and public attempts."""
import json, collections
ROW = ["cloud","cloud_no_solver","anchor","kernel","browserbase","browserless_solver","steel","hyperbrowser"]
page = json.load(open("data/page_grid.json"))
att = collections.defaultdict(dict)
for l in open("data/attempts.jsonl"):
    r = json.loads(l); att[r["task_id"]].setdefault(r["configuration"], []).append(r)
def sig(t):
    out = []
    for c in ROW:
        rs = att[t][c]
        out.append("u" if all(r["score"] is None for r in rs) else str(sum(r["classification"] == "accessible" for r in rs)))
    return "".join(out)
cols = ["".join(page[r][c] for r in range(8)) for c in range(100)]
sigs = {t: sig(t) for t in sorted(att)}
assert sorted(cols) == sorted(sigs.values()), "page grid and attempts disagree"
pool = collections.defaultdict(list)
for t in sorted(att): pool[sigs[t]].append(t)
json.dump([pool[s].pop(0) for s in cols], open("data/site_order.json", "w"))
print("order ok")
