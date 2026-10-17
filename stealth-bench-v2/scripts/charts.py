"""Builds the Stealth Bench v2 images in one quiet style: flat colours, hairlines, no glow."""
import json, collections
D = json.load(open("data/final_data.json")); sites = D["sites"]; ov = D["overall"]
SOLVER = [("cloud","Browser Use Cloud"),("anchor","Anchor"),("kernel","Kernel"),("browserbase","Browserbase"),("browserless_solver","Browserless"),("steel","Steel"),("hyperbrowser","Hyperbrowser")]
REF = [("headful_proxy","Chrome + US proxy"),("headless_direct","Headless Chrome")]
VCOL = {"Cloudflare":"#D9823F","Akamai":"#5B9BD5","DataDome":"#55B07E","PerimeterX / HUMAN":"#A68BE0","Kasada":"#D96C8C","Not identified":"#6E6E76"}
LOGO = {"Cloudflare":("logos/cloudflare/cloudflare.png",30),"Akamai":("logos/akamai/akamai.svg",22),"DataDome":("logos/datadome/datadome.svg",17),"PerimeterX / HUMAN":("logos/human/human-dark.svg",22),"Kasada":("logos/kasada/kasada.svg",19)}
def fmt(v, d=1): return (f"{v:.{d}f}".rstrip("0").rstrip(".") if d else f"{v:.0f}") + "%"
vend = collections.Counter(s["vendor"] for s in sites)
VORDER = sorted(vend, key=lambda v: (v == "Not identified", -vend[v]))
def brand(v, small=False):
    if v not in LOGO: return '<span class="vn">Not identified</span>'
    f, h = LOGO[v]
    if small: h = round(h * .82)
    out = f'<img class="logo" src="{f}" style="height:{h}px">'
    if v == "Akamai": out += '<span class="vn">Akamai</span>'
    if v.startswith("Perimeter"): out += '<span class="alt">PerimeterX</span>'
    return out
MARK = '<svg viewBox="0 0 28 44" width="17" height="27"><path d="M13.5 1.5 2 22l11 20.5 2.1-18.3-3.7-4.8Z" fill="#F2F2F0"/><path d="m15.2 2.2-2 16.9 3.8 4.7-2.1 18.7L26 22Z" fill="#F2F2F0" opacity=".7"/></svg>'
TOP = f'<div class="top"><div class="brand">{MARK}<span>Distilled</span></div><div class="tag">Stealth Bench v2 (browser-use)</div></div>'
FOOT = ('<div class="foot"><span>* Visits to sites that were down or unreachable are left out: 3 of 200 with the solver, 2 of 200 without. '
        "Other providers' site and network errors are left out the same way.<br>Others: Browser Use, Stealth Bench v2, Sept 25, 2026. "
        'Distilled: our own runs; 15 visits in the solver run were retried once.</span><b>distilled.cx</b></div>')
BASE = '''
@font-face{font-family:"Distilled Sans";src:url(DistilledSans.woff2) format("woff2");font-weight:100 700}
:root{--fg:#F2F2F0;--fg2:#A3A3AA;--fg3:#6E6E76;--line:rgba(255,255,255,.09);--bar:#48484E;--dim:#2A2A2E}
*{box-sizing:border-box;margin:0}
body{width:1600px;height:900px;overflow:hidden;position:relative;background:#0A0A0B;color:var(--fg);font-family:"Distilled Sans",sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
canvas{position:absolute;inset:0;width:1600px;height:900px}
.top{position:absolute;left:88px;right:88px;top:62px;display:flex;justify-content:space-between;align-items:center}
.brand{display:flex;align-items:center;gap:11px;font-weight:500;font-size:23px;letter-spacing:-.01em}
.tag{font-size:18px;color:var(--fg2)}
.h1{position:absolute;left:88px;top:136px;font-weight:500;font-size:46px;letter-spacing:-.025em;line-height:1.05}
.sub{position:absolute;left:88px;top:196px;font-size:19px;color:var(--fg2)}
.foot{position:absolute;left:88px;right:88px;bottom:38px;display:flex;justify-content:space-between;align-items:flex-end;gap:40px;font-size:13.5px;line-height:1.6;color:var(--fg3)}
.foot b{font-weight:500;font-size:16px;color:var(--fg2);white-space:nowrap}
.logo{filter:brightness(0) invert(1);display:block;opacity:.92}
.vn{font-size:19px;font-weight:500;color:var(--fg)} .alt{font-size:13px;color:var(--fg3)}
'''
SHADER = '''
const c=document.getElementById("bg"),gl=c.getContext("webgl");
const vs="attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
const fs=`precision highp float;uniform vec2 r;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
void main(){
 vec2 uv=gl_FragCoord.xy/r; vec2 p=uv*vec2(r.x/r.y,1.);
 float d=length(p-vec2(1.62,1.22));
 float light=exp(-d*d*1.35)*.105;
 float low=(n(p*1.3)-.5)*.010;
 float v=.036+light+low;
 v+=(h(gl_FragCoord.xy)-.5)*.013;
 gl_FragColor=vec4(vec3(v),1.);
}`;
function sh(t,s){const o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);return o;}
const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);gl.useProgram(pr);
const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
const l=gl.getAttribLocation(pr,"p");gl.enableVertexAttribArray(l);gl.vertexAttribPointer(l,2,gl.FLOAT,false,0,0);
gl.uniform2f(gl.getUniformLocation(pr,"r"),c.width,c.height);gl.viewport(0,0,c.width,c.height);gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
'''
def page(name, css, body, foot=FOOT):
    open(name, "w").write(f'<!doctype html><meta charset="utf-8"><style>{BASE}{css}</style><canvas id="bg" width="3200" height="1800"></canvas>{TOP}{body}{foot}<script>{SHADER}</script>')

# ---- 1. the 20 hardest sites ----
hard = sites[-20:]
def hrate(f):
    p = sum(f(s)[0] for s in hard); n = sum(f(s)[1] for s in hard); return p / n * 100
hb = [("Distilled", "", hrate(lambda s: s["distilled"]), "me"), ("Distilled", "no solver", hrate(lambda s: s["distilled_ns"]), "me2")]
hb += [(n, "", hrate(lambda s, c=c: s["others"][c]), "") for c, n in SOLVER]
hb += [("Browser Use Cloud", "no solver", hrate(lambda s: s["others"]["cloud_no_solver"]), "")]
hb.sort(key=lambda b: -b[2])
best_other = max(v for n, sub, v, cls in hb if cls == "")
H = 410
cols = "".join(f'<div class="col {cls}"><div class="bv" style="bottom:{v/100*H + 12:.1f}px">{fmt(v)}</div><div class="bar" style="height:{v/100*H:.1f}px"></div>'
               f'<div class="bn">{n}{f"<span>{sub}</span>" if sub else ""}</div></div>' for n, sub, v, cls in hb)
grid = "".join(f'<div class="gl" style="bottom:{g/100*H:.1f}px"><span>{g}%</span></div>' for g in (0, 25, 50, 75, 100))
hard_css = f'''
.chart{{position:absolute;left:88px;right:88px;top:306px;height:{H}px}}
.gl{{position:absolute;left:0;right:0;height:0;border-top:1px solid rgba(255,255,255,.07)}}
.gl span{{position:absolute;left:0;top:-9px;font-size:13px;color:var(--fg3)}}
.cols{{position:absolute;left:58px;right:0;bottom:0;top:0;display:flex;justify-content:space-between}}
.col{{position:relative;width:96px;height:100%}}
.bar{{position:absolute;left:12px;right:12px;bottom:0;background:#46464C;border-radius:2px 2px 0 0}}
.bv{{position:absolute;left:0;right:0;text-align:center;font-size:21px;font-weight:500;color:var(--fg2)}}
.bn{{position:absolute;left:-14px;right:-14px;top:{H + 14}px;text-align:center;font-size:15px;line-height:1.3;color:var(--fg2)}}
.bn span{{display:block;color:var(--fg3)}}
.col.me .bar{{background:var(--fg)}} .col.me .bv{{color:var(--fg);font-size:30px}} .col.me .bn{{color:var(--fg);font-weight:500}}
.col.me2 .bar{{background:rgba(242,242,240,.55)}} .col.me2 .bv{{color:var(--fg)}} .col.me2 .bn{{color:var(--fg)}}
'''
hard_foot = ('<div class="foot"><span>Hardest: the last 20 sites in Browser Use\'s site-by-site ranking, which is set by their own providers\' results. '
             'No Distilled visits were left out on these sites;<br>other providers\' site and network errors are left out. '
             'Others: Browser Use, Stealth Bench v2, Sept 25, 2026. Distilled: our own runs; 15 visits in the solver run were retried once.</span><b>distilled.cx</b></div>')
page("1-hardest-20.html", hard_css, f'''<div class="h1">100% on the 20 hardest sites</div>
<div class="sub">Share of visits that got through, two visits per site. No other provider got above {fmt(best_other)}.</div>
<div class="chart">{grid}<div class="cols">{cols}</div></div>''', hard_foot)

# ---- 2. overall leaderboard ----
def hrow(name, v, cls="", label=None):
    return f'<div class="r {cls}"><div class="n">{name}</div><div class="t"><div class="b" style="width:{v:.2f}%"></div></div><div class="v">{label or fmt(v)}</div></div>'
solver_rows = hrow("Distilled", 100, "me", "100%*") + "".join(hrow(n, ov["others"][c][2]) for c, n in sorted(SOLVER, key=lambda x: -ov["others"][x[0]][2]))
nos = sorted([("Distilled", ov["distilled_ns"][2], "me"), ("Browser Use Cloud", ov["others"]["cloud_no_solver"][2], "")], key=lambda x: -x[1])
nos_rows = "".join(hrow(n, v, cls, (fmt(v) + "*") if cls == "me" else None) for n, v, cls in nos)
ref_rows = "".join(hrow(n, ov["others"][c][2], "ref") for c, n in REF)
lb_css = '''
.hl{position:absolute;left:88px;top:196px;width:560px}
.k{font-size:18px;color:var(--fg2)}
.big{font-weight:500;font-size:172px;line-height:1;letter-spacing:-.045em;margin:20px 0 0 -7px;white-space:nowrap}
.big sup{font-size:58px;letter-spacing:0;vertical-align:top;position:relative;top:16px;margin-left:8px;color:var(--fg2)}
.cap{margin-top:24px;font-size:23px;line-height:1.4;color:var(--fg2);max-width:460px}
.second{margin-top:46px;padding-top:28px;border-top:1px solid var(--line);max-width:470px}
.n2{font-weight:500;font-size:54px;letter-spacing:-.03em;line-height:1}
.n2 sup{font-size:24px;vertical-align:top;margin-left:4px;color:var(--fg2)}
.k2{margin-top:10px;font-size:19px;color:var(--fg2)}
.tbl{position:absolute;left:740px;right:88px;top:196px}
.sec{font-size:15px;color:var(--fg3);padding-bottom:9px;border-bottom:1px solid var(--line);margin-bottom:4px}
.sec.s2{margin-top:24px}
.r{display:grid;grid-template-columns:230px 1fr 96px;column-gap:18px;align-items:center;height:36px}
.n{font-size:19px;color:var(--fg2);white-space:nowrap}
.t{height:6px;background:rgba(255,255,255,.055);border-radius:1px}
.b{height:100%;background:var(--bar);border-radius:1px}
.v{font-size:19px;font-weight:500;color:var(--fg2);text-align:right}
.r.me .n,.r.me .v{color:var(--fg)} .r.me .n{font-weight:500} .r.me .b{background:var(--fg)}
.r.ref .n,.r.ref .v{color:var(--fg3)} .r.ref .b{background:var(--dim)}
'''
page("2-overall.html", lb_css, f'''
<div class="hl"><div class="k">With a CAPTCHA solver</div><div class="big">100%<sup>*</sup></div>
<div class="cap">of visits got through on 100 bot&#8209;protected sites, two visits each.</div>
<div class="second"><div class="n2">{fmt(ov["distilled_ns"][2])}<sup>*</sup></div><div class="k2">of visits got through without a solver.</div></div></div>
<div class="tbl"><div class="sec">With a CAPTCHA solver</div>{solver_rows}<div class="sec s2">Without a CAPTCHA solver</div>{nos_rows}<div class="sec s2">No stealth, for reference</div>{ref_rows}</div>''')

# ---- 3. site by site ----
def cs(t):
    p, n = t
    return "u" if n == 0 else ("f" if p == n else ("x" if p == 0 else "h"))
def grow(name, f, me, pctv, label=None):
    cells = "".join(f'<i class="{cs(f(s))}"></i>' for s in sites)
    return f'<div class="gr {"me" if me else ""}"><div class="n">{name}</div><div class="m">{cells}</div><div class="p">{label or fmt(pctv)}</div></div>'
strip = "".join(f'<i style="background:{VCOL[s["vendor"]]}"></i>' for s in sites)
g_solver = grow("Distilled", lambda s: s["distilled"], True, 100, "100%*") + "".join(grow(n, lambda s, c=c: s["others"][c], False, ov["others"][c][2]) for c, n in sorted(SOLVER, key=lambda x: -ov["others"][x[0]][2]))
g_nos = grow("Distilled", lambda s: s["distilled_ns"], True, ov["distilled_ns"][2], fmt(ov["distilled_ns"][2]) + "*") + grow("Browser Use Cloud", lambda s: s["others"]["cloud_no_solver"], False, ov["others"]["cloud_no_solver"][2])
leg = "".join(f'<div class="li"><b style="background:{VCOL[v]}"></b>{brand(v, True)}<span class="lc">{vend[v]}</span></div>' for v in VORDER)
grid_css = '''
.gw{position:absolute;left:88px;right:88px;top:250px}
.strip,.gr{display:grid;grid-template-columns:220px 1fr 84px;column-gap:16px;align-items:center}
.strip{height:16px;margin-bottom:6px}.strip .n{font-size:13.5px;color:var(--fg3)}
.m{display:grid;grid-template-columns:repeat(100,1fr);gap:2px;height:100%}
.strip .m{height:6px}.strip i{border-radius:1px}
.gsec{font-size:14px;color:var(--fg3);padding:12px 0 7px;border-bottom:1px solid var(--line);margin-bottom:6px}
.gr{height:22px;margin-bottom:5px}
.gr .n{font-size:17px;color:var(--fg2);white-space:nowrap}
.gr .p{font-size:17px;font-weight:500;color:var(--fg2);text-align:right}
.gr i{border-radius:1px;background:#18181B}
.gr i.f{background:#55555C}.gr i.h{background:#323237}
.gr i.u{background:transparent;outline:1px dashed #4A4A50;outline-offset:-1px}
.gr.me .n,.gr.me .p{color:var(--fg);font-weight:500}
.gr.me i.f{background:var(--fg)}.gr.me i.h{background:rgba(242,242,240,.38)}
.gax{display:grid;grid-template-columns:220px 1fr 84px;column-gap:16px;margin-top:8px;font-size:13.5px;color:var(--fg3)}
.gax .a{display:flex;justify-content:space-between}
.legend{position:absolute;left:88px;right:88px;top:688px;display:flex;gap:38px;align-items:center;padding-top:18px;border-top:1px solid var(--line)}
.li{display:flex;align-items:center;gap:10px}
.li b{width:9px;height:9px;border-radius:1px}
.lc{font-size:14px;color:var(--fg3);margin-left:2px}
.li .vn{font-size:16px}
'''
page("3-site-by-site.html", grid_css, f'''<div class="h1">100%<span style="color:var(--fg2)">*</span> across all 100 sites</div>
<div class="sub">One column per site, easiest to hardest in Browser Use's order. The strip on top is each site's protection.</div>
<div class="gw"><div class="strip"><div class="n">Protection</div><div class="m">{strip}</div><div></div></div>
<div class="gsec">With a CAPTCHA solver</div>{g_solver}<div class="gsec">Without a CAPTCHA solver</div>{g_nos}
<div class="gax"><div></div><div class="a"><span>Easiest</span><span>Light: every counted visit got through &nbsp;·&nbsp; Mid: one of two &nbsp;·&nbsp; Dark: blocked &nbsp;·&nbsp; Dashed: none counted</span><span>Hardest</span></div><div></div></div></div>
<div class="legend">{leg}</div>''')

# ---- 4. by protection ----
def vrate(ss, f):
    p = sum(f(s)[0] for s in ss); n = sum(f(s)[1] for s in ss); return p / n * 100
COLS = [("Distilled", lambda s: s["distilled"], "c1"), ("Browser Use Cloud", lambda s: s["others"]["cloud"], "c3")]
prow = ""
for v in VORDER:
    ss = [s for s in sites if s["vendor"] == v]
    cells = ""
    for i, (_, f, cls) in enumerate(COLS):
        x = vrate(ss, f)
        starred = i == 0 and any(f(s)[1] < 2 for s in ss)
        cells += f'<div class="cell {cls}"><div class="val">{fmt(x, 0)}{"*" if starred else ""}</div><div class="trk"><div class="fill" style="width:{x:.2f}%"></div></div></div>'
    oth = [vrate(ss, lambda s, c=c: s["others"][c]) for c, _ in SOLVER[1:]]
    ticks = "".join(f'<i style="left:{x:.2f}%"></i>' for x in oth)
    cells += (f'<div class="cell c5"><div class="val">{fmt(min(oth), 0)}–{fmt(max(oth), 0)}</div>'
              f'<div class="trk rng"><div class="span" style="left:{min(oth):.2f}%;width:{max(oth)-min(oth):.2f}%"></div>{ticks}</div></div>')
    prow += f'<div class="pr"><div class="pv"><div class="pb">{brand(v)}</div><div class="pc">{vend[v]} sites</div></div>{cells}</div>'
heads = "".join(f'<div>{n}</div>' for n, _, _ in COLS) + '<div>Other providers<br>(lowest–highest)</div>'
prot_css = '''
.ptbl{position:absolute;left:88px;right:88px;top:262px}
.ph,.pr{display:grid;grid-template-columns:280px repeat(3,1fr);column-gap:64px;align-items:center}
.ph{font-size:14px;line-height:1.3;color:var(--fg3);padding-bottom:10px;border-bottom:1px solid var(--line);align-items:end}
.pr{height:78px;border-bottom:1px solid var(--line)}
.pb{display:flex;align-items:center;gap:8px;height:30px}
.pc{font-size:14px;color:var(--fg3);margin-top:3px}
.val{font-size:25px;font-weight:500;color:var(--fg2);letter-spacing:-.01em}
.trk{position:relative;height:4px;margin-top:9px;background:rgba(255,255,255,.06);border-radius:1px}
.fill{height:100%;border-radius:1px}
.c1 .val,.c2 .val{color:var(--fg)}
.c1 .fill{background:var(--fg)} .c2 .fill{background:rgba(242,242,240,.5)}
.c3 .fill{background:#74747C} .c4 .fill{background:#4E4E55}
.rng .span{position:absolute;top:0;bottom:0;background:#3E3E44}
.rng i{position:absolute;top:-3px;width:1px;height:10px;background:#8A8A92}
'''
page("4-by-protection.html", prot_css, f'''<div class="h1">100%<span style="color:var(--fg2)">*</span> against every protection</div>
<div class="sub">Share of visits that got through with a CAPTCHA solver, by the protection on the site.</div>
<div class="ptbl"><div class="ph"><div>Protection</div>{heads}</div>{prow}</div>''')
print("hardest 20:", [(n, sub, round(v, 1)) for n, sub, v, _ in hb])
