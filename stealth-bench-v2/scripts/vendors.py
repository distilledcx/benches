"""Labels each site's bot protection from one plain GET: headers, cookies and page source. Writes task_id -> vendor only."""
import base64, hashlib, json, os, re, subprocess, tempfile, collections, concurrent.futures as cf
from cryptography.fernet import Fernet
key = base64.urlsafe_b64encode(hashlib.sha256(b"Stealth_Bench_V2").digest())
raw = Fernet(key).decrypt(base64.b64decode(open("private/Stealth_Bench_V2.enc").read()))
assert hashlib.sha256(raw).hexdigest() == json.load(open("data/protocol.json"))["dataset_sha256"]
tasks = json.loads(raw)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
SIGS = {
    "Cloudflare": [r"cf-ray:", r"server:\s*cloudflare", r"cf-mitigated", r"challenges\.cloudflare\.com", r"cdn-cgi/challenge-platform", r"__cf_bm", r"cf_clearance"],
    "Akamai": [r"server:\s*akamaighost", r"\b_abck\b", r"\bak_bmsc\b", r"\bbm_sz\b", r"\bbm_sv\b", r"akamai-grn", r"/akam/\d+"],
    "DataDome": [r"x-datadome", r"\bdatadome=", r"captcha-delivery\.com", r"js\.datadome\.co", r"dd_cookie_test"],
    "PerimeterX / HUMAN": [r"px-captcha", r"\b_px[0-9a-z]*=", r"perimeterx", r"px-cdn\.net", r"px-client\.net", r"captcha\.px-cdn"],
    "Imperva": [r"incap_ses", r"visid_incap", r"x-iinfo", r"x-cdn:\s*imperva", r"_incapsula_resource"],
    "Kasada": [r"x-kpsdk", r"/ips\.js", r"kpsdk"],
    "F5 / Shape": [r"\bts01[0-9a-f]{6,}", r"_imp_apg_r_", r"shape security", r"x-[a-z0-9]{8}-[abcdz]:"],
    "AWS WAF": [r"x-amzn-waf", r"aws-waf-token", r"awswaf"],
}
CHALLENGE = {
    "Cloudflare": r"just a moment|attention required|cf-mitigated:\s*challenge|checking your browser",
    "DataDome": r"captcha-delivery\.com|datadome",
    "PerimeterX / HUMAN": r"px-captcha|press (&|and) hold|human verification",
    "Akamai": r"reference #\d+\.|access denied.*akamai|errors\.edgesuite\.net",
    "Imperva": r"incapsula incident|_incapsula_resource",
    "Kasada": r"kpsdk",
    "AWS WAF": r"awswaf|aws-waf",
}
DEDICATED = ["DataDome", "PerimeterX / HUMAN", "Kasada", "Akamai", "Imperva", "F5 / Shape"]
def probe(task):
    d = tempfile.mkdtemp(); h, b, j = (os.path.join(d, n) for n in "hbj")
    try:
        p = subprocess.run(["curl", "-sS", "-L", "--max-redirs", "5", "--max-time", "25", "--compressed", "-A", UA,
                            "-H", "Accept: text/html,application/xhtml+xml", "-H", "Accept-Language: en-US,en;q=0.9",
                            "-D", h, "-o", b, "-c", j, "-w", "%{http_code}", task["website"]], capture_output=True, text=True, timeout=40)
        status = p.stdout or "000"
    except subprocess.TimeoutExpired:
        status = "000"
    read = lambda f: open(f, "rb").read(400000).decode("utf-8", "ignore") if os.path.exists(f) else ""
    headers, body, jar = read(h), read(b), read(j)
    blob = (headers + "\n" + jar + "\n" + body).lower()
    found = [v for v, pats in SIGS.items() if any(re.search(x, blob) for x in pats)]
    challenge = [v for v, pat in CHALLENGE.items() if re.search(pat, (body + headers + jar).lower()) and status in ("403", "429", "503", "202", "401", "000")]
    ded = [v for v in challenge if v != "Cloudflare"]
    vendor = ded[0] if ded else ("Cloudflare" if challenge else next((v for v in DEDICATED if v in found), "Cloudflare" if "Cloudflare" in found else "Not identified"))
    return task["task_id"], vendor
with cf.ThreadPoolExecutor(8) as ex:
    out = dict(ex.map(probe, tasks))
json.dump(out, open("data/vendors.json", "w"), indent=1, sort_keys=True)
print(dict(collections.Counter(out.values()).most_common()))
