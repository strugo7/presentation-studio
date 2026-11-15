# -*- coding: utf-8 -*-
"""blueprint.json -> a self-contained HTML deck folder.

Fixed 1920x1080 stage, camera-flight navigation (smooth zoom between slides; tiles on an agenda/hub
slide fly into their section), staged reveals, RTL-aware, optional embedded font. Charts/tables/
diagrams rendered inline (no libraries). Pure stdlib + optional Pillow for image copy.

Usage:  python render_html.py blueprint.json out_dir [assets_dir] [--font path.ttf] [--pdf]
          --pdf  => also emit a print-friendly build (static, for Chrome --print-to-pdf)
"""
import sys, os, json, html, base64, shutil, math

args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = [a for a in sys.argv[1:] if a.startswith("--")]
BP = json.load(open(args[0], encoding="utf-8"))
OUT = args[1]
ASSETS = args[2] if len(args) > 2 else os.path.dirname(os.path.abspath(args[0]))
FONT = None
for f in flags:
    if f.startswith("--font="): FONT = f.split("=", 1)[1]
PDF = "--pdf" in flags
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

meta = BP.get("meta", {}); RTL = bool(meta.get("rtl")); LANG = meta.get("language", "en")
d = BP.get("design", {})
pal = {**{"bg": "FFFFFF", "bgAlt": "F6F7F9", "ink": "1A2230", "mute": "5B6472", "accent": "2C5F7C",
          "accent2": "B4722E", "hair": "E2E5EA", "dark": "1C2A3A"}, **d.get("palette", {})}
fonts = {**{"display": "Assistant", "body": "Assistant", "mono": "ui-monospace,Menlo,monospace"}, **d.get("fonts", {})}
slides = BP.get("slides", [])
sections = BP.get("sections", [])
nav = BP.get("navigation", {})
ZOOM = nav.get("mode") == "zoom"
E = html.escape

def asset_src(ref):
    if not ref: return None
    for a in BP.get("assets", []):
        if a.get("id") == ref and a.get("path"):
            p = a["path"]; src = p if os.path.isabs(p) else os.path.join(ASSETS, p)
            if os.path.exists(src):
                dst = "assets/" + os.path.basename(src); shutil.copy(src, os.path.join(OUT, dst)); return dst
    src = ref if os.path.isabs(ref) else os.path.join(ASSETS, ref)
    if os.path.exists(src):
        dst = "assets/" + os.path.basename(src); shutil.copy(src, os.path.join(OUT, dst)); return dst
    return None

# ---------- exhibits (inline, no libs) ----------
def svg_bar(data):
    cats = data.get("categories", []); series = data.get("series", [{}])
    vals = series[0].get("values", []) if series else []
    mx = max(vals + [1]); n = len(cats); W, H = 900, 560; pad = 70
    bw = (W - 2*pad) / max(n, 1) * 0.55
    bars = []
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = pad + (W - 2*pad) * (i + 0.5) / max(n, 1) - bw/2
        bh = (H - 2*pad) * v / mx; y = H - pad - bh
        col = pal["accent2"] if i == len(cats)-1 else pal["accent"]
        bars.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="8" fill="#{col}"/>'
                    f'<text x="{x+bw/2:.0f}" y="{y-14:.0f}" text-anchor="middle" font-size="30" font-weight="800" fill="#{pal["ink"]}">{E(str(v))}</text>'
                    f'<text x="{x+bw/2:.0f}" y="{H-pad+36:.0f}" text-anchor="middle" font-size="26" fill="#{pal["mute"]}">{E(str(c))}</text>')
    return (f'<svg viewBox="0 0 {W} {H}" style="width:100%;height:auto">'
            f'<line x1="{pad}" y1="{H-pad}" x2="{W-pad}" y2="{H-pad}" stroke="#{pal["hair"]}" stroke-width="2"/>'
            + "".join(bars) + '</svg>')

def table_html(data):
    cols = data.get("columns", []); rows = data.get("rows", [])
    if RTL: cols = list(reversed(cols)); rows = [list(reversed(r)) for r in rows]
    th = "".join(f"<th>{E(str(c))}</th>" for c in cols)
    trs = "".join("<tr>" + "".join(f"<td>{E(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="ex-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def diagram_html(data):
    steps = data.get("steps", [])
    if RTL: steps = list(reversed(steps))
    cells = []
    for i, s in enumerate(steps):
        last = (not RTL and i == len(steps)-1) or (RTL and i == 0)
        cells.append(f'<div class="node {"last" if last else ""}"><div class="nn">{(len(steps)-i) if RTL else i+1:02d}</div><div class="nm">{E(str(s))}</div></div>')
    return '<div class="chain">' + "".join(cells) + '</div>'

def exhibit_html(ex):
    if not ex: return ""
    t = ex.get("type"); cap = ex.get("caption", "")
    inner = ""
    if t in ("image", "screenshot"):
        src = asset_src(ex.get("ref"))
        inner = f'<div class="frame"><img src="{src}" alt=""></div>' if src else f'<div class="frame ph">[{E(ex.get("ref") or "image")}]</div>'
    elif t == "chart": inner = f'<div class="frame chart">{svg_bar(ex.get("data", {}))}</div>'
    elif t == "table": inner = table_html(ex.get("data", {}))
    elif t == "diagram": return f'<div class="diagram">{diagram_html(ex.get("data", {}))}{f"<div class=cap>{E(cap)}</div>" if cap else ""}</div>'
    elif t == "code": inner = '<pre class="frame code">' + E(str(ex.get("data", ""))) + '</pre>'
    capdiv = f'<figcaption>{E(cap)}</figcaption>' if cap else ""
    return f'<figure class="shot">{inner}{capdiv}</figure>'

# ---------- bullets ----------
def bullets_html(bs, reveal_base=0):
    out = []
    for i, b in enumerate(bs or []):
        lead = f'<b>{E(b["lead"])}</b> ' if b.get("lead") else ""
        out.append(f'<li data-rk="bullet:{i}">{lead}{E(b.get("text",""))}</li>')
    return '<ul class="pts">' + "".join(out) + "</ul>" if out else ""

# ---------- reveal wiring ----------
def reveal_attrs(sl):
    # map reveal tokens to data-step on elements; returns (max_step)
    steps = sl.get("animation", {}).get("reveals", [])
    tok_step = {}
    for r in steps:
        for tok in r.get("show", []): tok_step[tok] = r.get("step", 1)
    return tok_step, (max([r.get("step", 1) for r in steps], default=0))

def with_steps(body_html, tok_step):
    # inject data-step on elements carrying data-rk that are in tok_step
    import re
    def rep(m):
        rk = m.group(1)
        return f' data-rk="{rk}"' + (f' data-step="{tok_step[rk]}"' if rk in tok_step else "")
    return re.sub(r' data-rk="([^"]+)"', rep, body_html)

# ---------- slide renderers ----------
def slide_section(sl):
    role = sl.get("role", "concept")
    dark = sl.get("dark", role in ("cover", "stakes", "close", "quote", "divider"))
    bgk = (sl.get("background") or {}); photo = asset_src(bgk.get("photo"))
    cls = "slide " + ("dark" if dark else "light")
    tok_step, mx = reveal_attrs(sl)
    title = E(sl.get("actionTitle", "")); kicker = E(sl.get("kicker", ""))
    bg = ""
    if photo: bg = f'<div class="photo" style="background-image:url({photo})"></div><div class="scrim"></div>'
    body = ""
    if role == "cover":
        body = (f'<div class="c cover"><div class="col">'
                f'{f"<div class=eyebrow>{kicker}</div>" if kicker else ""}'
                f'<h1>{title or E(meta.get("title",""))}</h1>'
                f'{f"<div class=sub>{E(meta.get(chr(34)+chr(34).join(["subtitle"]))) if False else E(meta.get("subtitle",""))}</div>" if meta.get("subtitle") else ""}'
                f'{f"<div class=team>{(chr(32)+chr(183)+chr(32)).join(E(a) for a in meta.get("authors",[]))}</div>" if meta.get("authors") else ""}'
                f'</div></div>')
    elif role in ("stakes", "close", "quote", "divider"):
        extra = "".join(f'<p data-rk="bullet:{i}">{E(b.get("text",""))}</p>' for i, b in enumerate(sl.get("bullets", [])))
        body = f'<div class="c statement"><div class="col"><h2>{title}</h2>{extra}</div></div>'
    elif role == "agenda":
        tiles = []
        tmap = {s["id"]: s for s in slides}
        for i, sec in enumerate(sections):
            first = (sec.get("slideIds") or [None])[0]
            goto = (next((j for j, s in enumerate(slides) if s["id"] == first), 0)) if first else 0
            tiles.append(f'<div class="tile" data-goto="{goto}"><div class="tn">{i+1:02d}</div><div class="ts">{E(sec.get("title",""))}</div></div>')
        body = (f'<div class="hd"><div class="kicker">{kicker}</div><h2 class="title">{title}</h2></div>'
                f'<div class="bd"><div class="tiles">{"".join(tiles)}</div></div>')
    else:
        ex = sl.get("exhibit"); bl = bullets_html(sl.get("bullets", []))
        exh = exhibit_html(ex)
        if role in ("references", "appendix"):
            lis = "".join(f'<li>{E(b.get("text",""))}</li>' for b in sl.get("bullets", []))
            body = f'<div class="hd"><div class="kicker">{kicker}</div><h2 class="title">{title}</h2></div><div class="bd"><ul class="refs">{lis}</ul></div>'
        elif ex and ex.get("type") in ("diagram",) or role == "process":
            body = f'<div class="hd"><div class="kicker">{kicker}</div><h2 class="title">{title}</h2></div><div class="bd proc">{exh}{bl}</div>'
        elif ex and ex.get("type") == "table" or role == "comparison":
            body = f'<div class="hd"><div class="kicker">{kicker}</div><h2 class="title">{title}</h2></div><div class="bd">{exh}</div>'
        elif ex:
            side = ex.get("side", "left")
            cols = f'<div class="vis" data-rk="exhibit">{exh}</div><div class="txt">{bl}</div>'
            if side == "right": cols = f'<div class="txt">{bl}</div><div class="vis" data-rk="exhibit">{exh}</div>'
            body = f'<div class="hd"><div class="kicker">{kicker}</div><h2 class="title">{title}</h2></div><div class="bd"><div class="two">{cols}</div></div>'
        else:
            body = f'<div class="hd"><div class="kicker">{kicker}</div><h2 class="title">{title}</h2></div><div class="bd">{bl}</div>'
    body = with_steps(body, tok_step)
    notes = f'<aside class="notes">{E(sl.get("speakerNotes",""))}</aside>' if sl.get("speakerNotes") else ""
    return f'<section class="{cls}" data-max="{mx}" data-title="{E(sl.get("kicker") or role)}">{bg}<div class="ov"></div>{body}{notes}</section>'

SECTIONS_HTML = "".join(slide_section(s) for s in slides)

# rows for the camera grid: one row per section (fallback: all in one row)
rows = []
if sections:
    idset = {s["id"]: i for i, s in enumerate(slides)}
    used = set()
    for sec in sections:
        r = [idset[x] for x in sec.get("slideIds", []) if x in idset]; used |= set(r)
        if r: rows.append(r)
    leftover = [i for i in range(len(slides)) if i not in used]
    if leftover: rows.append(leftover)
else:
    rows = [list(range(len(slides)))]
ROWS = [len(r) for r in rows]
ORDER = [i for r in rows for i in r]  # linear reading order follows rows

font_face = ""
if FONT and os.path.exists(FONT):
    b64 = base64.b64encode(open(FONT, "rb").read()).decode()
    font_face = f'@font-face{{font-family:"{fonts["display"]}";src:url(data:font/ttf;base64,{b64}) format("truetype");font-weight:200 800}}'
else:
    font_face = '@import url("https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap");'

HTML = r'''<!DOCTYPE html><html lang="''' + LANG + '"' + (' dir="rtl"' if RTL else '') + r'''><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>''' + E(meta.get("title", "Deck")) + r'''</title><style>
''' + font_face + r'''
:root{--bg:#''' + pal["bg"] + r''';--bgAlt:#''' + pal["bgAlt"] + r''';--ink:#''' + pal["ink"] + r''';--mute:#''' + pal["mute"] + r''';
--accent:#''' + pal["accent"] + r''';--accent2:#''' + pal["accent2"] + r''';--hair:#''' + pal["hair"] + r''';--dark:#''' + pal["dark"] + r''';
--disp:"''' + fonts["display"] + r'''",system-ui,sans-serif;--mono:''' + fonts["mono"] + r''';--ease:cubic-bezier(.65,0,.2,1)}
*{margin:0;padding:0;box-sizing:border-box}html,body{height:100%;overflow:hidden;background:#0b141d;font-family:var(--disp)}
.vp{position:fixed;inset:0;overflow:hidden}.stage{position:absolute;width:1920px;height:1080px;transform-origin:0 0;overflow:hidden;background:var(--dark)}
.world{position:absolute;transform-origin:0 0}
.slide{position:absolute;width:1920px;height:1080px;overflow:hidden;''' + ('direction:rtl;text-align:right' if RTL else 'text-align:left') + r''';box-shadow:0 40px 120px rgba(0,0,0,.45)}
.slide.light{background:var(--bg);color:var(--ink);background-image:linear-gradient(rgba(44,95,124,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(44,95,124,.05) 1px,transparent 1px);background-size:40px 40px}
.slide.dark{background:var(--dark);color:#fff}
.photo{position:absolute;inset:-4%;background-size:cover;background-position:center;filter:saturate(.8)}
.scrim{position:absolute;inset:0;background:linear-gradient(''' + ('270deg' if RTL else '90deg') + r''',rgba(28,42,58,.96),rgba(28,42,58,.62) 70%,rgba(28,42,58,.4))}
.hd{position:absolute;right:110px;left:110px;top:74px;z-index:2}.kicker{font-size:28px;font-weight:700;color:var(--accent);margin-bottom:10px}
.title{font-size:70px;font-weight:800;line-height:1.05;color:var(--ink)}.bd{position:absolute;right:110px;left:110px;top:300px;bottom:130px;z-index:2}
.two{display:grid;grid-template-columns:5fr 6fr;gap:70px;height:100%;align-items:center}.vis{min-width:0}.txt{min-width:0}
.pts{list-style:none}.pts li{position:relative;font-size:34px;line-height:1.35;color:var(--mute);margin-bottom:22px;padding-''' + ('right' if RTL else 'left') + r''':46px}
.pts li::before{content:"";position:absolute;''' + ('right' if RTL else 'left') + r''':0;top:.55em;width:16px;height:16px;border-radius:4px;background:var(--accent)}
.pts li b{color:var(--ink);font-weight:800}.refs{list-style:none}.refs li{font-size:26px;color:var(--mute);margin-bottom:14px}
.shot{background:#fff;border:1px solid var(--hair);border-radius:18px;padding:16px;box-shadow:0 20px 50px rgba(26,34,48,.14)}
.shot .frame{border-radius:10px;overflow:hidden;background:#0f1a26;display:flex;align-items:center;justify-content:center;min-height:200px}
.shot .frame.chart{background:#fff;padding:14px}.shot .frame.ph{color:#8aa;font-family:var(--mono);padding:60px}
.shot img{display:block;max-width:100%;max-height:560px}.shot figcaption{font-size:22px;color:var(--mute);margin-top:10px}
pre.code{color:#cfe;font-family:var(--mono);font-size:22px;padding:24px;text-align:left;direction:ltr;overflow:auto}
.ex-table{width:100%;border-collapse:collapse;font-size:28px}.ex-table th{background:var(--dark);color:#fff;font-weight:700;padding:20px;text-align:''' + ('right' if RTL else 'left') + r'''}
.ex-table td{padding:20px;color:var(--mute);border-bottom:1px solid var(--hair)}.ex-table tbody tr:nth-child(odd){background:var(--bgAlt)}
.ex-table td:first-child{color:var(--ink);font-weight:700}
.diagram .chain{display:flex;gap:16px;align-items:stretch}.diagram .node{flex:1;background:#fff;border:1px solid var(--hair);border-radius:18px;padding:26px 16px;text-align:center;box-shadow:0 14px 34px rgba(26,34,48,.1)}
.node .nn{font:700 24px var(--mono);color:var(--accent)}.node .nm{font-size:30px;font-weight:800;color:var(--ink);margin-top:8px}
.node.last{background:var(--dark)}.node.last .nn{color:var(--accent2)}.node.last .nm{color:#fff}.diagram .cap{margin-top:22px;font-size:26px;color:var(--mute)}
.cover .col{position:absolute;right:140px;left:140px;top:50%;transform:translateY(-52%)}.eyebrow{font-size:30px;font-weight:700;color:var(--accent);margin-bottom:18px}
.cover h1{font-size:150px;font-weight:800;line-height:.98;color:#fff;letter-spacing:-.02em}.cover .sub{font-size:44px;color:#cdd6de;margin-top:26px}.cover .team{font-size:34px;font-weight:700;color:var(--accent);margin-top:44px}
.statement .col{position:absolute;right:140px;left:140px;top:50%;transform:translateY(-52%)}.statement h2{font-size:96px;font-weight:800;line-height:1.1;color:#fff}.statement p{font-size:38px;color:#aeb9c4;margin-top:28px}
.tiles{display:flex;gap:40px;height:100%;align-items:center}.tile{flex:1;height:460px;border-radius:24px;padding:40px;cursor:pointer;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.16);transition:transform .4s,border-color .3s}
.slide.light .tile{background:#fff;border-color:var(--hair)}.tile:hover{transform:translateY(-10px);border-color:var(--accent2)}.tile .tn{font-size:90px;font-weight:800;color:var(--accent2)}.tile .ts{font-size:48px;font-weight:800;color:#fff;margin-top:14px}.slide.light .tile .ts{color:var(--ink)}
.notes{display:none}.ov{display:none}
[data-step]{opacity:0;transform:translateY(26px);transition:opacity .6s var(--ease),transform .8s var(--ease)}
.slide.in [data-step].on{opacity:1;transform:none}
.hud{position:fixed;left:0;right:0;bottom:20px;display:flex;justify-content:center;z-index:50;opacity:0;transition:.4s}body.ui .hud{opacity:1}
.hud .box{background:rgba(14,22,32,.82);backdrop-filter:blur(8px);border-radius:999px;padding:8px 16px;color:#cfd8e2;font-size:16px;font-weight:600;display:flex;gap:14px}
.hud button{background:none;border:0;color:#cfd8e2;font:inherit;cursor:pointer}.hud button:hover{color:#fff}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:34vh;overflow:auto;background:rgba(14,22,32,.95);color:#e8eef3;padding:24px 8vw;font-size:24px;line-height:1.5;transform:translateY(100%);transition:.4s;z-index:60;''' + ('direction:rtl' if RTL else '') + r'''}#notes.open{transform:none}
body.overview .slide{cursor:pointer}body.overview .ov{display:block;position:absolute;''' + ('left' if RTL else 'right') + r''':40px;top:20px;font-size:180px;font-weight:800;color:var(--accent2);z-index:9}
@media print{@page{size:1920px 1080px;margin:0}html,body{height:auto;overflow:visible}.vp{position:static}.stage{position:static;transform:none!important;width:1920px;height:auto}.world{position:static;transform:none!important}
.slide{position:relative!important;left:auto!important;top:auto!important;break-after:page;box-shadow:none}[data-step]{opacity:1!important;transform:none!important}.hud,#notes{display:none}}
</style></head><body>
<div class="vp"><div class="stage" id="stage"><div class="world" id="world">''' + SECTIONS_HTML + r'''</div></div></div>
<div class="hud"><div class="box"><span id="count"></span><button data-a="map">Map</button><button data-a="ov">Overview</button><button data-a="n">Notes</button><button data-a="f">Full</button></div></div>
<div id="notes"></div>
<script>
const ROWS=''' + json.dumps(ROWS) + r''', ORDER=''' + json.dumps(ORDER) + r''', ZOOM=''' + ("true" if ZOOM else "false") + r''';
const HUB=''' + json.dumps(next((i for i, s in enumerate(slides) if s.get("role") == "agenda"), 0)) + r''';
const SW=1920,SH=1080,GX=520,GY=520,stage=document.getElementById('stage'),world=document.getElementById('world');
const slides=[...document.querySelectorAll('.slide')];
const pos=[];let k=0;ROWS.forEach((n,r)=>{for(let c=0;c<n;c++){const idx=ORDER[k++];pos[idx]={x:c*(SW+GX),y:r*(SH+GY)};}});
slides.forEach((s,i)=>{s.style.left=pos[i].x+'px';s.style.top=pos[i].y+'px';const o=s.querySelector('.ov');if(o)o.textContent=String(i+1).padStart(2,'0');});
function layout(){const f=Math.min(innerWidth/SW,innerHeight/SH);stage.style.transform=`translate(${(innerWidth-SW*f)/2}px,${(innerHeight-SH*f)/2}px) scale(${f})`;}
addEventListener('resize',layout);layout();
const cam={cx:SW/2,cy:SH/2,k:1};function apply(){world.style.transform=`translate(${SW/2-cam.cx*cam.k}px,${SH/2-cam.cy*cam.k}px) scale(${cam.k})`;}
const tgt=i=>({cx:pos[i].x+SW/2,cy:pos[i].y+SH/2,k:1});
let raf=0,fid=0;
function vw(w0,w1,d,rho){const r2=rho*rho,r4=r2*r2;const b0=(w1*w1-w0*w0+r4*d*d)/(2*w0*r2*d),b1=(w1*w1-w0*w0-r4*d*d)/(2*w1*r2*d);const r0=Math.log(Math.sqrt(b0*b0+1)-b0),r1=Math.log(Math.sqrt(b1*b1+1)-b1);const S=(r1-r0)/rho;return{S,f:t=>{const s=t*S,u=(w0/r2)*Math.cosh(r0)*Math.tanh(rho*s+r0)-(w0/r2)*Math.sinh(r0);return{u:u/d,w:w0*Math.cosh(r0)/Math.cosh(rho*s+r0)};}};}
function fly(to,inst){cancelAnimationFrame(raf);const id=++fid,fr={...cam};if(inst){Object.assign(cam,to);apply();return Promise.resolve();}
const w0=SW/fr.k,w1=SW/to.k,dx=to.cx-fr.cx,dy=to.cy-fr.cy,dd=Math.hypot(dx,dy);let S,f;
if(dd<2){const L=Math.log(w1/w0);S=Math.abs(L)/1.35+.001;f=t=>({u:0,w:w0*Math.exp(L*t)});}else{const o=vw(w0,w1,dd,1.35);S=o.S;f=o.f;}
const dur=Math.min(2400,Math.max(1000,S*600)),t0=performance.now();
return new Promise(res=>{const st=now=>{if(id!==fid)return res();let t=Math.min(1,(now-t0)/dur);const e=t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,r=f(e);cam.cx=fr.cx+(dd<2?0:dx*r.u);cam.cy=fr.cy+(dd<2?0:dy*r.u);cam.k=SW/r.w;apply();if(t<1)raf=requestAnimationFrame(st);else{Object.assign(cam,to);apply();res();}};raf=requestAnimationFrame(st);});}
let idx=0,step=0,ov=false;
function setStep(i,s){slides[i].querySelectorAll('[data-step]').forEach(e=>e.classList.toggle('on',+e.dataset.step<=s));step=s;}
function maxStep(i){return +slides[i].dataset.max||0;}
function activate(i){slides.forEach((s,j)=>s.classList.toggle('in',j===i));document.getElementById('count').textContent=(i+1)+' / '+slides.length;const n=slides[i].querySelector('.notes');document.getElementById('notes').textContent=n?n.textContent:'';}
function go(i,opt){opt=opt||{};i=Math.max(0,Math.min(slides.length-1,i));if(ov){ov=false;document.body.classList.remove('overview');}idx=i;setStep(i,opt.step==='max'?maxStep(i):0);fly(tgt(i),opt.inst).then(()=>activate(i));if(opt.inst)activate(i);}
function next(){if(ov)return;if(step<maxStep(idx))setStep(idx,step+1);else if(idx<slides.length-1)go(idx+1);}
function prev(){if(ov)return;if(step>0)setStep(idx,step-1);else if(idx>0)go(idx-1,{step:'max'});}
function overview(){if(ov){go(idx);return;}ov=true;document.body.classList.add('overview');slides.forEach(s=>s.classList.add('in'));
const cols=Math.max(...ROWS),W=cols*SW+(cols-1)*GX,H=ROWS.length*SH+(ROWS.length-1)*GY;fly({cx:W/2,cy:H/2,k:Math.min(SW/(W+300),SH/(H+300))});}
document.addEventListener('click',e=>{const a=e.target.closest('[data-a]');if(a){({map:()=>go(HUB),ov:overview,n:()=>document.getElementById('notes').classList.toggle('open'),f:()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()})[a.dataset.a]();return;}
if(ov){const s=e.target.closest('.slide');if(s)go(slides.indexOf(s));return;}
const g=e.target.closest('[data-goto]');if(g){go(+g.dataset.goto);return;}});
addEventListener('keydown',e=>{const k=e.key;if([' ','ArrowRight','ArrowDown','PageDown','Enter'].includes(k)){e.preventDefault();next();}else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(k))prev();else if(k==='m'||k==='M')go(HUB);else if(k==='o'||k==='O')overview();else if(k==='n'||k==='N')document.getElementById('notes').classList.toggle('open');else if(k==='f'||k==='F')document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();else if(k==='Escape'){document.getElementById('notes').classList.remove('open');if(ov)go(idx);}});
let it;addEventListener('mousemove',()=>{document.body.classList.add('ui');clearTimeout(it);it=setTimeout(()=>document.body.classList.remove('ui'),2500);});
(document.fonts?document.fonts.ready:Promise.resolve()).then(()=>go(0,{inst:true}));
window.deck={go,next,prev,overview};
</script></body></html>'''

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("saved", os.path.join(OUT, "index.html"), "| slides:", len(slides), "| rtl:", RTL, "| zoom:", ZOOM)
