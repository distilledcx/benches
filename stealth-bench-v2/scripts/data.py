"""Per-site and overall results for every provider, with site and network errors left out for everyone."""
import json, collections
ERR = {"site_error", "network_error"}
att = collections.defaultdict(lambda: collections.defaultdict(list))
for l in open("data/attempts.jsonl"):
    r = json.loads(l); att[r["task_id"]][r["configuration"]].append(r["classification"])
order = json.load(open("data/site_order.json"))
vend = json.load(open("data/vendors.json"))
# Distilled with its solver (run of Oct 16-17): every visit got through except these errors.
NATIVE_ERR = {"shs100-058": ["site_error", "site_error"], "shs100-075": ["accessible", "network_error"]}
# Distilled with no solver (run of Oct 15-16): visits that got through, of two, where not two.
NS_ACC = {"shs100-008":1,"shs100-012":0,"shs100-013":1,"shs100-029":1,"shs100-040":1,"shs100-042":0,"shs100-044":1,"shs100-047":1,"shs100-049":1,
          "shs100-058":0,"shs100-065":0,"shs100-070":0,"shs100-071":1,"shs100-073":0,"shs100-079":1,"shs100-088":0,"shs100-093":0,"shs100-099":0}
NS_ERR = {"shs100-058": 2}
PROV = ["cloud","cloud_no_solver","anchor","kernel","browserbase","browserless_solver","steel","hyperbrowser","headful_proxy","headless_direct"]
def tally(cls):
    counted = [c for c in cls if c not in ERR]
    return sum(c == "accessible" for c in counted), len(counted)
sites = []
for t in order:
    sites.append({"task_id": t, "vendor": vend[t],
                  "distilled": tally(NATIVE_ERR.get(t, ["accessible", "accessible"])),
                  "distilled_ns": (NS_ACC.get(t, 2), 2 - NS_ERR.get(t, 0)),
                  "others": {c: tally(att[t][c]) for c in PROV}})
def overall(f):
    p = sum(f(s)[0] for s in sites); n = sum(f(s)[1] for s in sites); return p, n, p / n * 100
out = {"distilled": overall(lambda s: s["distilled"]), "distilled_ns": overall(lambda s: s["distilled_ns"]),
       "others": {c: overall(lambda s, c=c: s["others"][c]) for c in PROV}}
json.dump({"sites": sites, "overall": out}, open("data/final_data.json", "w"))
for k in ("distilled", "distilled_ns"): print(k, out[k])
for c in PROV: print(c, out["others"][c])
