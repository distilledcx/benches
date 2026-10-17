"""5:2 cover for the X article, in the same style as the charts."""
VALS = [("Distilled", 100.0, True), ("Browser Use Cloud", 91.4, False), ("Kernel", 82.1, False), ("Anchor", 82.0, False),
        ("Browserbase", 79.3, False), ("Browserless", 77.9, False), ("Steel", 74.5, False), ("Hyperbrowser", 73.5, False)]
def fmt(v): return f"{v:.1f}".rstrip("0").rstrip(".") + "%"
H = 300
bars = "".join(f'<div class="c {"me" if me else ""}"><div class="v" style="bottom:{v/100*H+10:.0f}px">{fmt(v)}</div>'
               f'<div class="b" style="height:{v/100*H:.1f}px"></div><div class="n">{n}</div></div>' for n, v, me in VALS)
MARK = '<svg viewBox="0 0 28 44" width="17" height="27"><path d="M13.5 1.5 2 22l11 20.5 2.1-18.3-3.7-4.8Z" fill="#F2F2F0"/><path d="m15.2 2.2-2 16.9 3.8 4.7-2.1 18.7L26 22Z" fill="#F2F2F0" opacity=".7"/></svg>'
CSS = f'''
@font-face{{font-family:"Distilled Sans";src:url(DistilledSans.woff2) format("woff2");font-weight:100 700}}
:root{{--fg:#F2F2F0;--fg2:#A3A3AA;--fg3:#6E6E76}}
*{{box-sizing:border-box;margin:0}}
body{{width:1500px;height:600px;overflow:hidden;position:relative;background:#0A0A0B;color:var(--fg);font-family:"Distilled Sans",sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}}
canvas{{position:absolute;inset:0;width:1500px;height:600px}}
.top{{position:absolute;left:72px;right:72px;top:52px;display:flex;justify-content:space-between;align-items:center}}
.brand{{display:flex;align-items:center;gap:11px;font-weight:500;font-size:23px;letter-spacing:-.01em}}
.tag{{font-size:18px;color:var(--fg2)}}
.big{{position:absolute;left:72px;top:176px;font-weight:500;font-size:128px;letter-spacing:-.045em;line-height:1}}
.cap{{position:absolute;left:72px;top:330px;width:540px;font-size:25px;line-height:1.4;color:var(--fg2)}}
.chart{{position:absolute;right:72px;top:178px;width:690px;height:{H}px;border-bottom:1px solid rgba(255,255,255,.14);display:flex;justify-content:space-between;align-items:flex-end}}
.c{{position:relative;width:62px;height:100%}}
.b{{position:absolute;left:10px;right:10px;bottom:0;background:#46464C;border-radius:2px 2px 0 0}}
.v{{position:absolute;left:-10px;right:-10px;text-align:center;font-size:15px;font-weight:500;color:var(--fg2)}}
.n{{position:absolute;left:-18px;right:-18px;top:{H+10}px;text-align:center;font-size:12.5px;line-height:1.2;color:var(--fg3)}}
.c.me .b{{background:var(--fg)}} .c.me .v{{color:var(--fg);font-size:19px}} .c.me .n{{color:var(--fg)}}
'''
SHADER = '''
const c=document.getElementById("bg"),gl=c.getContext("webgl");
const vs="attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
const fs=`precision highp float;uniform vec2 r;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
void main(){
 vec2 uv=gl_FragCoord.xy/r; vec2 p=uv*vec2(r.x/r.y,1.);
 float d=length(p-vec2(r.x/r.y*.92,1.22));
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
BODY = f'''<div class="top"><div class="brand">{MARK}<span>Distilled</span></div><div class="tag">Stealth Bench v2 (browser-use)</div></div>
<div class="big">197 of 197</div>
<div class="cap">visits got through on Browser Use's Stealth Bench v2, from a Distilled cloud phone with a CAPTCHA solver.</div>
<div class="chart">{bars}</div>'''
open("cover.html", "w").write(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><canvas id="bg" width="3000" height="1200"></canvas>{BODY}<script>{SHADER}</script>')
