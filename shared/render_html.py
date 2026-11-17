# -*- coding: utf-8 -*-
"""blueprint.json -> a self-contained HTML deck folder.

Fixed 1920x1080 stage, camera-flight navigation (smooth zoom between slides; tiles on an agenda/hub
slide fly into their section), staged reveals, RTL-aware, embedded font (works offline: no CDN).
Design-system tokens drive composition (layout, type scale, motif, exhibit frame). Charts (column,
bar, line, scatter), tables and diagrams (chain, timeline, sequence) render inline with no libraries.
Quizzes/polls are real accessible controls with local feedback. prefers-reduced-motion is honoured.

Usage:  python render_html.py blueprint.json out_dir [assets_dir] [--font=path.ttf] [--pdf] [--no-embed-font]
          --pdf  => print build (static, every reveal shown, quiz answers as slides, for Chrome --print-to-pdf)
"""
import sys, os, json, html, base64, shutil, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import blueprint_lib as bl  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = [a for a in sys.argv[1:] if a.startswith("--")]
BP = bl.load(args[0])
OUT = args[1]
ASSETS = args[2] if len(args) > 2 else os.path.dirname(os.path.abspath(args[0]))
FONT = None
for f in flags:
    if f.startswith("--font="): FONT = f.split("=", 1)[1]
PDF = "--pdf" in flags
EMBED = "--no-embed-font" not in flags
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

meta = BP.get("meta", {}); RTL = bool(meta.get("rtl")); LANG = meta.get("language", "en")
S = bl.strings(LANG)
d = BP.get("design", {})
SYS, TOK = bl.resolve_system(d)
pal = bl.palette(d)
fonts = {**{"display": "Assistant", "body": "Assistant", "mono": "ui-monospace,Menlo,monospace"}, **d.get("fonts", {})}
slides = bl.expand_slides(BP, "print" if PDF else "live")
sections = BP.get("sections", [])
nav = BP.get("navigation", {})
ZOOM = nav.get("mode") == "zoom"
RM_META = bool((meta.get("accessibility") or {}).get("reducedMotion"))
A = bl.Assets(BP, ASSETS)
E = html.escape
START, END = ("right", "left") if RTL else ("left", "right")

def asset_src(ref):
    src = A.file_for(ref)
    if not src: return None
    name = A.dest_name(ref, src); dst = os.path.join(OUT, "assets", name)
    if not os.path.exists(dst): shutil.copy(src, dst)
    return "assets/" + name

def sec_index(sl):
    for i, s in enumerate(sections):
        if sl.get("section") == s.get("id") or sl.get("id") in (s.get("slideIds") or []): return i + 1
    return None

def link(text, url):
    if bl.is_safe_url(url):
        return f'<a href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(text)}</a>'
    return E(text)

# ---------- charts (inline SVG, same spec as the PPTX builder) ----------
SER, HL, BASE1 = bl.chart_colors(pal)   # distinct series inks; highlight always differs from the base

def _legend(sp, W, y):
    if len(sp["series"]) < 2: return ""
    out, x = [], 90
    for i, s in enumerate(sp["series"]):
        out.append(f'<rect x="{x}" y="{y-16}" width="20" height="20" rx="4" fill="#{SER[i % 4]}"/>'
                   f'<text x="{x+30}" y="{y}" font-size="28" fill="#{pal["mute"]}">{E(s["name"])}</text>')
        x += 80 + 17 * len(s["name"])
    return "".join(out)

def _axis_labels(sp, W, H, L, B):
    o = ""
    yl = sp["yLabel"] or sp["unit"]
    if sp["kind"] == "bar":
        # Horizontal bars: the value axis runs along the bottom and the category labels fill the
        # start column, so a rotated label at x=22 would sit on top of them. An explicit yLabel goes
        # under the bars (the unit alone is already printed on every value), xLabel above the labels.
        if sp["yLabel"]: o += f'<text x="{(L + W - 100) / 2:.0f}" y="{H - B + 46}" font-size="26" fill="#{pal["mute"]}" text-anchor="middle" class="ax-v">{E(yl)}</text>'
        if sp["xLabel"]: o += f'<text x="{L - 16}" y="{(70 if len(sp["series"]) > 1 else 40) - 12}" font-size="24" fill="#{pal["mute"]}" text-anchor="end" class="ax-c">{E(sp["xLabel"])}</text>'
        return o
    if yl: o += f'<text x="22" y="{(H-B)/2+20:.0f}" font-size="26" fill="#{pal["mute"]}" text-anchor="middle" transform="rotate(-90 22 {(H-B)/2+20:.0f})">{E(yl)}</text>'
    if sp["xLabel"]: o += f'<text x="{(W+L)/2:.0f}" y="{H-12}" font-size="26" fill="#{pal["mute"]}" text-anchor="middle">{E(sp["xLabel"])}</text>'
    return o

def svg_chart(data):
    sp = bl.chart_spec(data)
    if sp["kind"] == "unsupported":
        return table_html(bl.table_from_chart(sp)) + f'<div class="cap">({E(sp["requested"])} → table)</div>'
    W, H = 1000, 600
    T = 70 if len(sp["series"]) > 1 else 40
    L, R, B = 100, 40, 90
    dec, unit = sp["decimals"], sp["unit"]
    k = sp["kind"]
    body = []
    if k == "scatter":
        pts = [p for s in sp["series"] for p in s["points"]]
        xs = [p[0] for p in pts] or [0]; ys = [p[1] for p in pts] or [0]
        xmx, ymx = bl.nice_max(max(xs)), bl.nice_max(max(ys)); xmn = min(0, min(xs)); ymn = min(0, min(ys))
        X = lambda v: L + (W-L-R) * (v - xmn) / ((xmx - xmn) or 1); Y = lambda v: H - B - (H-B-T) * (v - ymn) / ((ymx - ymn) or 1)
        for i in range(5):
            v = ymn + (ymx-ymn)*i/4; y = Y(v)
            body.append(f'<line x1="{L}" y1="{y:.0f}" x2="{W-R}" y2="{y:.0f}" stroke="#{pal["hair"]}" stroke-width="1.5"/><text x="{L-12}" y="{y+8:.0f}" text-anchor="end" font-size="26" fill="#{pal["mute"]}">{E(bl.fmt_num(v, dec))}</text>')
            xv = xmn + (xmx-xmn)*i/4
            body.append(f'<text x="{X(xv):.0f}" y="{H-B+34}" text-anchor="middle" font-size="26" fill="#{pal["mute"]}">{E(bl.fmt_num(xv, dec))}</text>')
        for si, s in enumerate(sp["series"]):
            for p in s["points"]:
                body.append(f'<circle cx="{X(p[0]):.0f}" cy="{Y(p[1]):.0f}" r="9" fill="#{SER[si % 4]}" fill-opacity=".85"/>')
                if len(p) > 2: body.append(f'<text x="{X(p[0])+14:.0f}" y="{Y(p[1])-10:.0f}" font-size="20" fill="#{pal["ink"]}">{E(str(p[2]))}</text>')
    else:
        cats = sp["categories"]; n = max(len(cats), 1); m = max(len(sp["series"]), 1)
        allv = [v for s in sp["series"] for v in s["values"]] or [0]
        base = sp["yMin"] if (k == "line" and sp["yMin"] is not None) else min(0, min(allv))
        vmn, vmx, vstep = bl.nice_ticks(max(allv), base)
        if k == "bar":
            L = 240
            X = lambda v: L + (W-L-R-60) * (v - vmn) / ((vmx - vmn) or 1)
            band = (H-T-B) / n
            for i, c in enumerate(cats):
                yc = T + band * (i + 0.5)
                body.append(f'<text x="{L-16}" y="{yc+9:.0f}" text-anchor="end" font-size="30" fill="#{pal["ink"]}">{E(str(c))}</text>')
                bh = band * 0.7 / m
                for si, s in enumerate(sp["series"]):
                    v = s["values"][i]; y = yc - band*0.35 + si*bh
                    col = (HL if sp["highlight"] == i else (BASE1 if sp["highlight"] is not None else SER[0])) if m == 1 else SER[si % 4]
                    x0, x1 = X(0), X(v)
                    body.append(f'<rect x="{min(x0,x1):.0f}" y="{y:.0f}" width="{abs(x1-x0):.0f}" height="{bh-6:.0f}" rx="4" fill="#{col}"/>'
                                f'<text x="{max(x0,x1)+10:.0f}" y="{y+bh/2+10:.0f}" font-size="30" font-weight="800" fill="#{pal["ink"]}">{E(bl.fmt_num(v, dec, unit))}</text>')
            body.append(f'<line x1="{X(0):.0f}" y1="{T}" x2="{X(0):.0f}" y2="{H-B}" stroke="#{pal["mute"]}" stroke-width="2"/>')
        else:
            Y = lambda v: H - B - (H-B-T) * (v - vmn) / ((vmx - vmn) or 1)
            nt = int(round((vmx - vmn) / vstep))
            for i in range(nt + 1):
                v = vmn + vstep * i; y = Y(v)
                body.append(f'<line x1="{L}" y1="{y:.0f}" x2="{W-R}" y2="{y:.0f}" stroke="#{pal["hair"]}" stroke-width="1.5"/><text x="{L-12}" y="{y+8:.0f}" text-anchor="end" font-size="26" fill="#{pal["mute"]}">{E(bl.fmt_num(v, 0 if float(v).is_integer() else dec))}</text>')
            band = (W-L-R) / n
            for i, c in enumerate(cats):
                body.append(f'<text x="{L+band*(i+.5):.0f}" y="{H-B+36}" text-anchor="middle" font-size="30" fill="#{pal["mute"]}">{E(str(c))}</text>')
            if k == "column":
                gw = band * 0.7; bw = gw / m
                for si, s in enumerate(sp["series"]):
                    for i, v in enumerate(s["values"]):
                        x = L + band*i + (band-gw)/2 + si*bw
                        col = (HL if sp["highlight"] == i else (BASE1 if sp["highlight"] is not None else SER[0])) if m == 1 else SER[si % 4]
                        y0, y1 = Y(0), Y(v)
                        body.append(f'<rect x="{x+3:.0f}" y="{min(y0,y1):.0f}" width="{bw-6:.0f}" height="{abs(y1-y0):.0f}" rx="6" fill="#{col}"/>'
                                    f'<text x="{x+bw/2:.0f}" y="{min(y0,y1)-12:.0f}" text-anchor="middle" font-size="{32 if m==1 else 26}" font-weight="800" fill="#{pal["ink"]}">{E(bl.fmt_num(v, dec, unit))}</text>')
                body.append(f'<line x1="{L}" y1="{Y(0):.0f}" x2="{W-R}" y2="{Y(0):.0f}" stroke="#{pal["mute"]}" stroke-width="2"/>')
            else:  # line
                for si, s in enumerate(sp["series"]):
                    pts = [(L + band*(i+.5), Y(v)) for i, v in enumerate(s["values"])]
                    col = SER[si % 4]
                    body.append(f'<polyline fill="none" stroke="#{col}" stroke-width="5" stroke-linejoin="round" points="{" ".join("%.0f,%.0f" % p for p in pts)}"/>')
                    for i, (x, y) in enumerate(pts):
                        body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#{col}"/>')
                        if i == len(pts)-1 or sp["highlight"] == i:
                            body.append(f'<text x="{x:.0f}" y="{y-18:.0f}" text-anchor="middle" font-size="30" font-weight="800" fill="#{pal["ink"]}">{E(bl.fmt_num(s["values"][i], dec, unit))}</text>')
    title = f'<text x="{L}" y="28" font-size="24" font-weight="700" fill="#{pal["ink"]}">{E(sp["title"])}</text>' if sp["title"] else ""
    return (f'<svg class="chart-svg" data-kind="{k}" viewBox="0 0 {W} {H}" role="img" aria-label="{E(sp["title"] or k)}" style="width:100%;height:auto">'
            + title + _legend(sp, W, 40 if sp["title"] else 30) + "".join(body) + _axis_labels(sp, W, H, L, B) + '</svg>')

def table_html(data):
    cols = data.get("columns", []); rows = data.get("rows", [])   # dir=rtl already mirrors the columns
    th = "".join(f"<th>{E(str(c))}</th>" for c in cols)
    trs = "".join("<tr>" + "".join(f"<td>{E(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="ex-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def diagram_html(data):
    kind = data.get("kind", "chain")
    if kind == "sequence": return svg_sequence(data)
    if kind == "timeline":
        evs = data.get("events") or [{"label": s} for s in data.get("steps", [])]
        cells = "".join(f'<div class="ev"><div class="dot"></div><div class="when">{E(str(e.get("when","")))}</div><div class="nm">{E(str(e.get("label","")))}</div></div>' for e in evs)
        return f'<div class="timeline">{cells}</div>'
    steps = data.get("steps", [])  # flex follows the slide's direction: step 1 sits at the reading start
    cells = []
    for i, s in enumerate(steps):
        cells.append(f'<div class="node {"last" if i == len(steps)-1 else ""}"><div class="nn">{i+1:02d}</div><div class="nm">{E(str(s))}</div></div>')
    return '<div class="chain">' + "".join(cells) + '</div>'

def svg_sequence(data):
    actors = data.get("actors", []); msgs = data.get("messages", [])
    n = max(len(actors), 1); W = 1500; top = 120; step = 96; H = top + 40 + step * len(msgs) + 30
    xs = {a: 130 + (W - 260) * (i / max(n - 1, 1)) for i, a in enumerate(actors)}
    if RTL: xs = {a: W - x for a, x in xs.items()}
    o = [f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#{pal["ink"]}"/></marker></defs>']
    for a, x in xs.items():
        o.append(f'<rect x="{x-130:.0f}" y="10" width="260" height="76" rx="10" fill="#{pal["dark"]}"/><text x="{x:.0f}" y="59" text-anchor="middle" font-size="32" font-weight="700" fill="#fff">{E(a)}</text>'
                 f'<line x1="{x:.0f}" y1="86" x2="{x:.0f}" y2="{H-10}" stroke="#{pal["hair"]}" stroke-width="3" stroke-dasharray="8 8"/>')
    for i, mm in enumerate(msgs):
        y = top + 30 + i * step; x1 = xs.get(mm.get("from"), 130); x2 = xs.get(mm.get("to"), W - 130)
        col = pal["accent2"] if mm.get("emphasis") else pal["ink"]
        o.append(f'<line x1="{x1:.0f}" y1="{y}" x2="{x2:.0f}" y2="{y}" stroke="#{col}" stroke-width="3" marker-end="url(#ah)"/>'
                 f'<text x="{(x1+x2)/2:.0f}" y="{y-14}" text-anchor="middle" font-size="30" fill="#{pal["ink"]}">{E(mm.get("label",""))}</text>')
    return f'<svg class="seq-svg" viewBox="0 0 {W} {H}" role="img" aria-label="sequence diagram" style="width:100%;height:auto">' + "".join(o) + '</svg>'

def exhibit_html(ex, bleed=False):
    if not ex: return ""
    t = ex.get("type"); cap = ex.get("caption", "")
    inner = ""
    if t in ("image", "screenshot"):
        src = asset_src(ex.get("ref"))
        alt = ex.get("alt") or A.alt(ex.get("ref"), cap)
        inner = f'<div class="frame img"><img src="{src}" alt="{E(alt)}"></div>' if src else f'<div class="frame ph">[{E(ex.get("ref") or "image")}]</div>'
    elif t == "chart": inner = f'<div class="frame chart">{svg_chart(ex.get("data", {}))}</div>'
    elif t == "table": inner = table_html(ex.get("data", {}))
    elif t == "diagram": return f'<div class="diagram">{diagram_html(ex.get("data", {}))}{f"<div class=cap>{E(cap)}</div>" if cap else ""}</div>'
    elif t == "code": inner = '<pre class="frame code">' + E(str(ex.get("data", ""))) + '</pre>'
    capdiv = f'<figcaption>{E(cap)}</figcaption>' if cap else ""
    return f'<figure class="shot{" bleed" if bleed else ""}">{inner}{capdiv}</figure>'

# ---------- bullets + engagement ----------
def bullets_html(bs, tag="ul"):
    out = []
    for i, b in enumerate(bs or []):
        lead = f'<b>{E(b["lead"])}</b> ' if b.get("lead") else ""
        cls = ' class="mono"' if b.get("mono") else ""
        out.append(f'<li data-rk="bullet:{i}"{cls}>{lead}{E(b.get("text",""))}</li>')
    return f'<{tag} class="pts">' + "".join(out) + f"</{tag}>" if out else ""

def engage_html(sl):
    eng = sl.get("engagement") or {}; t = eng.get("type")
    if not t or t == "none" or sl.get("_answerFor"): return ""
    opts = eng.get("options") or []; corr = eng.get("correctOptionId"); fb = eng.get("feedback") or {}
    label = {"poll": S["question"], "activity": S["activity"], "demo": S["demo"]}.get(t, S["question"])
    prompt = eng.get("prompt", "")
    h = f'<div class="eg-k">{E(label)}</div>' + (f'<p class="eg-p" id="eg-{E(sl["id"])}">{E(prompt)}</p>' if prompt else "")
    mode = "info"
    if opts and t in ("quiz", "question", "poll"):
        mode = "quiz" if corr else "poll"
        btns = []
        for o in opts:
            ok = o["id"] == corr
            f = fb.get(o["id"]) or (fb.get("correct") if ok else fb.get("incorrect")) or ""
            btns.append(f'<button type="button" class="opt" role="radio" aria-checked="false" data-opt="{E(o["id"])}" data-fb="{E(f)}">'
                        f'<span class="ot">{E(o.get("text",""))}</span><span class="bar"></span><span class="cnt"></span></button>')
        h += f'<div class="opts" role="radiogroup" aria-labelledby="eg-{E(sl["id"])}">' + "".join(btns) + '</div>'
        h += '<div class="eg-fb" aria-live="polite"></div>'
        if mode == "quiz":
            ctext = next((o.get("text", "") for o in opts if o["id"] == corr), "")
            expl = fb.get(corr) or fb.get("correct") or fb.get("explanation") or ""
            h += f'<button type="button" class="eg-reveal">{E(S["reveal"])}</button>'
            inline = (eng.get("answerPlacement") == "inline") or (meta.get("deliveryMode") == "self-read" and not eng.get("answerPlacement"))
            h += f'<div class="eg-ans{" inline" if inline else ""}"><b>{E(S["answer"])}:</b> {E(ctext)}{(" — " + E(expl)) if expl else ""}</div>'
        else:
            h += f'<div class="eg-note">{E(S["poll"])}</div>'
    elif t == "demo":
        if eng.get("assetRef"):
            src = asset_src(eng["assetRef"])
            if src: h += f'<img class="eg-img" src="{src}" alt="{E(A.alt(eng["assetRef"], prompt))}">'
        if eng.get("url"): h += f'<div class="eg-link">{link(eng["url"], eng["url"])}</div>'
    return f'<div class="engage" data-mode="{mode}" data-correct="{E(corr or "")}">{h}</div>'

# ---------- reveal wiring ----------
def reveal_attrs(sl):
    steps = (sl.get("animation") or {}).get("reveals", [])
    tok_step = {}
    for r in steps:
        for tok in r.get("show", []): tok_step[tok] = r.get("step", 1)
    return tok_step, (max([r.get("step", 1) for r in steps], default=0))

def with_steps(body_html, tok_step):
    def rep(m):
        rk = m.group(1)
        return f' data-rk="{rk}"' + (f' data-step="{tok_step[rk]}"' if rk in tok_step else "")
    return re.sub(r' data-rk="([^"]+)"', rep, body_html)

# ---------- slide renderers ----------
def kicker_html(sl, kicker):
    if TOK["kicker"] == "number" and sec_index(sl):
        return f'<div class="kicker"><span class="kn">{sec_index(sl):02d}</span>{(" — " + kicker) if kicker else ""}</div>'
    return f'<div class="kicker">{kicker}</div>' if kicker else ""

def head(sl, kicker, title):
    ls = bl.title_scale_for(sl.get("actionTitle", ""))
    return f'<div class="hd">{kicker_html(sl, kicker)}<h2 class="title" data-rk="title" style="--ls:{ls}">{title}</h2></div>'

def slide_section(sl):
    role = sl.get("role", "concept"); lay = sl.get("layout")
    dark = sl.get("dark", role in ("cover", "stakes", "close", "quote", "divider"))
    bgk = (sl.get("background") or {}); photo = asset_src(bgk.get("assetRef") or bgk.get("photo"))
    cls = "slide " + ("dark" if dark else "light") + (f" lay-{lay}" if lay else "") + f" role-{role}"
    tok_step, mx = reveal_attrs(sl)
    title = E(sl.get("actionTitle", "")); kicker = E(sl.get("kicker", ""))
    ex = sl.get("exhibit"); eng = engage_html(sl)
    bg = ""
    if photo: bg = f'<div class="photo" style="background-image:url({photo})" role="img" aria-label="{E(A.alt(bgk.get("assetRef"), ""))}"></div><div class="scrim"></div>'
    body = ""
    if role == "cover" and not lay:
        body = (f'<div class="c cover"><div class="col">'
                f'{f"<div class=eyebrow>{kicker}</div>" if kicker else ""}'
                f'<h1>{title or E(meta.get("title",""))}</h1>'
                f'{"<div class=sub>" + E(meta.get("subtitle","")) + "</div>" if meta.get("subtitle") else ""}'
                f'{"<div class=team>" + " · ".join(E(a) for a in meta.get("authors",[])) + "</div>" if meta.get("authors") else ""}'
                f'</div></div>')
    elif lay == "statement" or (not lay and role in ("stakes", "close", "quote", "divider")):
        extra = "".join(f'<p data-rk="bullet:{i}">{E(b.get("text",""))}</p>' for i, b in enumerate(sl.get("bullets", [])))
        num = f'<div class="bigsec">{sec_index(sl):02d}</div>' if role == "divider" and sec_index(sl) else ""
        body = f'<div class="c statement"><div class="col">{num}{kicker_html(sl, kicker) if lay else ""}<h2 data-rk="title">{title}</h2>{extra}{eng}</div></div>'
    elif lay == "big-number":
        bn = (ex or {}).get("bigNumber") or {}
        body = (f'<div class="bign"><div class="col">{kicker_html(sl, kicker)}'
                f'<div class="bn-v" data-rk="exhibit">{E(str(bn.get("value","")))}<span class="bn-u">{E(bn.get("unit",""))}</span></div>'
                f'{"<div class=bn-c>" + E(bn.get("context","")) + "</div>" if bn.get("context") else ""}'
                f'<h2 class="bn-t" data-rk="title">{title}</h2>{bullets_html(sl.get("bullets"))}{eng}</div></div>')
    elif lay == "split":
        side = (ex or {}).get("side", "left")
        img = ex and ex.get("type") == "image"
        vis = f'<div class="sp-vis{" fill" if img else ""}" data-rk="exhibit">{exhibit_html(ex, bleed=bool(img))}</div>'
        txt = f'<div class="sp-txt">{kicker_html(sl, kicker)}<h2 class="title" data-rk="title" style="--ls:{bl.title_scale_for(sl.get("actionTitle",""))*0.82:.2f}">{title}</h2>{bullets_html(sl.get("bullets"))}{eng}</div>'
        body = f'<div class="split side-{side}">{vis + txt if side == "left" else txt + vis}</div>'
    elif lay == "full-exhibit":
        strip = " · ".join(E(b.get("text", "")) for b in sl.get("bullets", []))
        body = (f'<div class="stack">{head(sl, kicker, title)}<div class="full"><div class="fx" data-rk="exhibit">{exhibit_html(ex)}</div>'
                + (f'<div class="strip" data-rk="bullet:0">{strip}</div>' if strip else "") + f'{eng}</div></div>')
    elif role == "agenda":
        tiles = []
        for i, sec in enumerate(sections):
            first = (sec.get("slideIds") or [None])[0]
            goto = (next((j for j, s in enumerate(slides) if s["id"] == first), 0)) if first else 0
            tiles.append(f'<button type="button" class="tile" data-goto="{goto}"><span class="tn">{i+1:02d}</span><span class="ts">{E(sec.get("title",""))}</span></button>')
        body = head(sl, kicker, title) + f'<div class="bd"><div class="tiles">{"".join(tiles)}</div></div>'
    else:
        bl_ = bullets_html(sl.get("bullets", []))
        exh = exhibit_html(ex)
        if role in ("references", "appendix"):
            if sl.get("_entries"):
                lis = "".join('<li>' + (f'<span class="rn">[{e["n"]}]</span> ' if e.get("n") else "")
                              + " — ".join(f"<bdi>{E(p)}</bdi>" for p in e["parts"])
                              + (f' — <a href="{E(e["url"])}" target="_blank" rel="noopener noreferrer"><bdi>{E(bl.url_label(e["url"]))}</bdi></a>' if e.get("url") else "")
                              + '</li>' for e in sl["_entries"])
            else:
                lis = "".join(f'<li>{E(b.get("text",""))}</li>' for b in sl.get("bullets", []))
            body = head(sl, kicker if kicker != title else "", title) + f'<div class="bd"><ol class="refs">{lis}</ol></div>'
        elif (ex and ex.get("type") == "diagram") or (role == "process" and ex):
            body = head(sl, kicker, title) + f'<div class="bd proc"><div data-rk="exhibit">{exh}</div>{bl_}{eng}</div>'
        elif (ex and ex.get("type") == "table") or (role == "comparison" and ex):
            body = head(sl, kicker, title) + f'<div class="bd"><div data-rk="exhibit">{exh}</div>{bl_}{eng}</div>'
        elif ex:
            side = ex.get("side", "left")
            vis = f'<div class="vis" data-rk="exhibit">{exh}</div>'; txt = f'<div class="txt">{bl_}{eng}</div>'
            body = head(sl, kicker, title) + f'<div class="bd"><div class="two side-{side}">{vis + txt if side == "left" else txt + vis}</div></div>'
        else:
            body = head(sl, kicker, title) + f'<div class="bd">{bl_}{eng}</div>'
    body = with_steps(body, tok_step)
    deco = ""
    si = sec_index(sl)
    if not dark and TOK["motif"] == "rule" and role not in ("cover",):
        st = next((s.get("title", "") for s in sections if si and s is sections[si-1]), "")
        deco += f'<div class="runhead"><span>{E(meta.get("title",""))}{(" · " + E(st)) if st else ""}</span><span class="pg"></span></div>'
    if not dark and TOK["motif"] == "numbers" and si and role not in ("references", "appendix"):
        deco += f'<div class="secnum" aria-hidden="true">{si:02d}</div>'
    foot = bl.slide_footer(BP, sl, bl.slide_asset_ids(sl))
    foot = f'<div class="foot"><cite>{E(foot)}</cite></div>' if foot and role not in ("references",) else ""
    notes = f'<aside class="notes">{E(sl.get("speakerNotes",""))}</aside>' if sl.get("speakerNotes") else ""
    return (f'<section class="{cls}" id="s-{E(sl["id"])}" data-max="{mx}" aria-roledescription="slide" aria-label="{E(sl.get("actionTitle") or role)}">'
            f'{bg}{deco}<div class="ov"></div>{body}{foot}{notes}</section>')

SECTIONS_HTML = "".join(slide_section(s) for s in slides)

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
ORDER = [i for r in rows for i in r]

# ---------- font: embedded, never a CDN (the deck must open offline) ----------
font_face = ""; stack = f'"{fonts["display"]}",'
if FONT and os.path.exists(FONT):
    b64 = base64.b64encode(open(FONT, "rb").read()).decode()
    font_face = f'@font-face{{font-family:"{fonts["display"]}";src:url(data:font/ttf;base64,{b64}) format("truetype");font-weight:200 800}}'
elif EMBED and os.path.exists(bl.DEFAULT_FONT):
    b64 = base64.b64encode(open(bl.DEFAULT_FONT, "rb").read()).decode()
    font_face = f'@font-face{{font-family:"PSDeck";src:url(data:font/ttf;base64,{b64}) format("truetype");font-weight:200 800}}'
    stack += '"PSDeck",'
stack += 'system-ui,"Segoe UI","Noto Sans Hebrew","Arial Hebrew",Arial,sans-serif'

M = TOK["margin"]; TS = TOK["titleScale"]; TW = TOK["titleWeight"]; BS = TOK["bodyScale"]; RAD = TOK["radius"]
LIGHT = pal[TOK["lightBg"]] if TOK["lightBg"] in pal else pal["bg"]
GRID = ("background-image:linear-gradient(rgba(44,95,124,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(44,95,124,.05) 1px,transparent 1px);background-size:40px 40px"
        if TOK["motif"] == "grid" else "")
FRAME = TOK["frame"]
BODYCLS = f'sys-{SYS} frame-{FRAME} motif-{TOK["motif"]} kick-{TOK["kicker"]} cover-{TOK["coverAlign"]}' + (" pdf" if PDF else "") + (" rm" if RM_META else "")

HTML = r'''<!DOCTYPE html><html lang="''' + E(LANG) + '"' + (' dir="rtl"' if RTL else '') + r'''><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>''' + E(meta.get("title", "Deck")) + r'''</title><style>
''' + font_face + r'''
:root{--bg:#''' + pal["bg"] + r''';--bgAlt:#''' + pal["bgAlt"] + r''';--ink:#''' + pal["ink"] + r''';--mute:#''' + pal["mute"] + r''';
--accent:#''' + pal["accent"] + r''';--accent2:#''' + pal["accent2"] + r''';--hair:#''' + pal["hair"] + r''';--dark:#''' + pal["dark"] + r''';--light:#''' + LIGHT + r''';
--disp:''' + stack + r''';--mono:''' + fonts["mono"] + r''';--ease:cubic-bezier(.65,0,.2,1);--m:''' + str(M) + r'''px;--ts:''' + str(TS) + r''';--tw:''' + str(TW) + r''';--bs:''' + str(BS) + r''';--r:''' + str(RAD) + r'''px}
*{margin:0;padding:0;box-sizing:border-box}html,body{height:100%;overflow:hidden;background:#0b141d;font-family:var(--disp)}
.vp{position:fixed;inset:0;overflow:hidden}.stage{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;overflow:hidden;background:var(--dark)}
.world{position:absolute;left:0;top:0;transform-origin:0 0;direction:ltr}
.slide{position:absolute;width:1920px;height:1080px;overflow:hidden;''' + ('direction:rtl;text-align:right' if RTL else 'text-align:left') + r''';box-shadow:0 40px 120px rgba(0,0,0,.45)}
.slide.light{background-color:var(--light);color:var(--ink);''' + GRID + r'''}
.slide.dark{background:var(--dark);color:#fff}
.photo{position:absolute;inset:-4%;background-size:cover;background-position:center;filter:saturate(.8)}
.scrim{position:absolute;inset:0;background:linear-gradient(''' + ('270deg' if RTL else '90deg') + r''',rgba(28,42,58,.96),rgba(28,42,58,.62) 70%,rgba(28,42,58,.4))}
.hd{position:absolute;right:var(--m);left:var(--m);top:74px;z-index:2}
.kicker{font-size:28px;font-weight:700;color:var(--accent);margin-bottom:12px}
.kick-caps .kicker{font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}.kick-number .kn{color:var(--accent);font-variant-numeric:tabular-nums}
.title{font-size:max(46px,calc(70px * var(--ts) * var(--ls,1)));font-weight:var(--tw);line-height:1.07;color:var(--ink);letter-spacing:-.01em}
.slide.dark .title{color:#fff}
.bd{position:absolute;right:var(--m);left:var(--m);top:300px;bottom:140px;z-index:2}
.two{display:grid;grid-template-columns:5fr 6fr;gap:70px;height:100%;align-items:center;direction:ltr}.two.side-right{grid-template-columns:6fr 5fr}
.two>*{direction:''' + ('rtl' if RTL else 'ltr') + r''';min-width:0}
.pts{list-style:none}.pts li{position:relative;font-size:calc(34px * var(--bs));line-height:1.35;color:var(--mute);margin-bottom:22px;padding-''' + START + r''':46px}
.pts li::before{content:"";position:absolute;''' + START + r''':0;top:.55em;width:16px;height:16px;border-radius:4px;background:var(--accent)}
.pts li b{color:var(--ink);font-weight:800}.pts li.mono{font-family:var(--mono);direction:ltr;unicode-bidi:isolate}
.refs{list-style:none;counter-reset:r}.refs li{font-size:25px;line-height:1.4;color:var(--mute);margin-bottom:14px}.refs a{color:var(--accent);text-decoration:underline;text-underline-offset:4px}
.shot{background:#fff;border:1px solid var(--hair);border-radius:var(--r);padding:16px;box-shadow:0 20px 50px rgba(26,34,48,.14)}
.frame-hairline .shot{box-shadow:none;padding:0;border-radius:var(--r)}.frame-hairline .shot figcaption{padding:10px 14px}
.frame-bleed .shot{background:none;border:0;box-shadow:none;padding:0}
.shot .frame{border-radius:calc(var(--r) * .6);overflow:hidden;background:#0f1a26;display:flex;align-items:center;justify-content:center;min-height:200px}
.shot .frame.chart{background:#fff;padding:14px}.frame-bleed .shot .frame.chart{background:none}.shot .frame.ph{color:#8aa;font-family:var(--mono);padding:60px}
.shot img{display:block;max-width:100%;max-height:560px}.shot figcaption{font-size:22px;color:var(--mute);margin-top:10px}
.chart-svg,.seq-svg{direction:ltr}svg text{unicode-bidi:plaintext}.refs .rn{font-weight:800;color:var(--ink);unicode-bidi:isolate}
pre.code{color:#cfe;font-family:var(--mono);font-size:22px;padding:24px;text-align:left;direction:ltr;unicode-bidi:plaintext;overflow:auto;white-space:pre-wrap}
.ex-table{width:100%;border-collapse:collapse;font-size:28px}.ex-table th{background:var(--dark);color:#fff;font-weight:700;padding:20px;text-align:''' + START + r'''}
.ex-table td{padding:20px;color:var(--mute);border-bottom:1px solid var(--hair)}.ex-table tbody tr:nth-child(odd){background:var(--bgAlt)}
.ex-table td:first-child{color:var(--ink);font-weight:700}
.proc .pts{margin-top:40px}
.diagram .chain{display:flex;gap:16px;align-items:stretch}.diagram .node{flex:1;background:#fff;border:1px solid var(--hair);border-radius:var(--r);padding:26px 16px;text-align:center;box-shadow:0 14px 34px rgba(26,34,48,.1)}
.frame-hairline .diagram .node,.frame-bleed .diagram .node{box-shadow:none}
.node .nn{font:700 24px var(--mono);color:var(--accent)}.node .nm{font-size:30px;font-weight:800;color:var(--ink);margin-top:8px}
.node.last{background:var(--dark)}.node.last .nn{color:var(--accent2)}.node.last .nm{color:#fff}.diagram .cap{margin-top:22px;font-size:26px;color:var(--mute)}
.timeline{display:flex;position:relative;padding-top:40px}.timeline::before{content:"";position:absolute;top:58px;left:0;right:0;height:3px;background:var(--hair)}
.timeline .ev{flex:1;position:relative;padding:0 10px}.timeline .dot{width:36px;height:36px;border-radius:50%;background:var(--accent);border:6px solid var(--light);position:relative;z-index:1}
.timeline .ev:last-child .dot{background:var(--accent2)}.timeline .when{font:800 28px var(--disp);color:var(--accent);margin-top:18px}.timeline .nm{font-size:28px;color:var(--ink);margin-top:6px;line-height:1.25}
.cover .col{position:absolute;right:calc(var(--m) + 30px);left:calc(var(--m) + 30px);top:50%;transform:translateY(-52%)}.cover-center .cover .col,.cover-center .statement .col{text-align:center}
.eyebrow{font-size:30px;font-weight:700;color:var(--accent);margin-bottom:18px}
.cover h1{font-size:calc(150px * var(--ts));font-weight:var(--tw);line-height:.98;color:#fff;letter-spacing:-.02em}.cover .sub{font-size:44px;color:#cdd6de;margin-top:26px}.cover .team{font-size:34px;font-weight:700;color:var(--accent);margin-top:44px}
.statement .col{position:absolute;right:calc(var(--m) + 30px);left:calc(var(--m) + 30px);top:50%;transform:translateY(-52%)}
.statement h2{font-size:calc(96px * var(--ts));font-weight:var(--tw);line-height:1.1;color:inherit}.statement p{font-size:38px;margin-top:28px}
.slide.dark .statement p{color:#aeb9c4}.slide.light .statement p{color:var(--mute)}.slide.light .statement h2{color:var(--ink)}
.bigsec{font-size:200px;font-weight:800;color:var(--accent2);line-height:1;margin-bottom:10px}
.bign .col{position:absolute;right:var(--m);left:var(--m);top:50%;transform:translateY(-50%)}
.bn-v{font-size:290px;font-weight:800;line-height:.9;color:var(--accent2);letter-spacing:-.03em;font-variant-numeric:tabular-nums;direction:ltr;unicode-bidi:isolate;display:inline-block}
.bn-u{font-size:110px;margin-inline-start:16px;color:var(--accent)}.bn-c{font-size:30px;color:var(--mute);margin-top:12px}
.bn-t{font-size:calc(58px * var(--ts));font-weight:var(--tw);line-height:1.12;margin:34px 0 26px;max-width:1500px;color:inherit}
.slide.light .bn-t{color:var(--ink)}
.split{position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr;direction:ltr}.split>*{direction:''' + ('rtl' if RTL else 'ltr') + r''';min-width:0}
.sp-vis{background:var(--bgAlt);display:flex;align-items:center;justify-content:center;padding:70px;overflow:hidden}
.sp-vis.fill{padding:0}.sp-vis.fill .shot,.sp-vis.fill .frame{width:100%;height:100%;border-radius:0;border:0;padding:0;box-shadow:none;background:none}
.sp-vis.fill img{width:100%;height:100%;max-height:none;object-fit:cover}.sp-vis.fill figcaption{position:absolute;bottom:0;padding:14px 24px;background:rgba(255,255,255,.88)}
.sp-vis>*{width:100%}.sp-vis .shot img{max-height:760px;margin:0 auto}.sp-vis{position:relative}
.sp-txt{padding:120px var(--m);display:flex;flex-direction:column;justify-content:center;position:relative;z-index:2}.sp-txt .title{margin-bottom:46px}
.stack{position:absolute;top:74px;bottom:120px;right:var(--m);left:var(--m);display:flex;flex-direction:column;z-index:2}.motif-rule .stack{top:96px}
.stack .hd{position:static;margin-bottom:34px}.full{flex:1;min-height:0;display:flex;flex-direction:column}
.full .fx{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}.full .fx>*{max-width:100%;max-height:100%}
.full .shot{display:flex;flex-direction:column;max-height:100%}.full .shot .frame{min-height:0}
.full .fx>*{width:100%}.full .chart-svg,.full .seq-svg{width:100%!important;height:560px!important}
.full .shot img{max-height:560px;margin:0 auto}.strip{font-size:28px;color:var(--mute);margin-top:14px}
.tiles{display:flex;gap:40px;height:100%;align-items:center}.tile{flex:1;height:460px;border-radius:24px;padding:40px;cursor:pointer;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.16);transition:transform .4s,border-color .3s;font:inherit;text-align:inherit;display:block}
.slide.light .tile{background:#fff;border-color:var(--hair)}.tile:hover,.tile:focus-visible{transform:translateY(-10px);border-color:var(--accent2)}.tile .tn{display:block;font-size:90px;font-weight:800;color:var(--accent2)}.tile .ts{display:block;font-size:48px;font-weight:800;color:#fff;margin-top:14px}.slide.light .tile .ts{color:var(--ink)}
.runhead{position:absolute;top:30px;right:var(--m);left:var(--m);display:flex;justify-content:space-between;font-size:20px;letter-spacing:.06em;color:var(--mute);padding-bottom:12px;border-bottom:1px solid var(--hair);z-index:2}
.motif-rule .hd{top:96px}.motif-numbers .slide.light .hd{padding-inline-end:250px}
.secnum{position:absolute;top:10px;''' + END + r''':50px;font-size:230px;font-weight:800;line-height:1;color:var(--hair);opacity:.7;z-index:0;font-variant-numeric:tabular-nums}
.foot{position:absolute;bottom:44px;right:var(--m);left:var(--m);font-size:19px;line-height:1.35;color:var(--mute);z-index:3}.foot cite{font-style:normal}
.slide.dark .foot{color:#9aa6b2}
.engage{margin-top:28px;padding:28px 32px;border:1.5px solid var(--hair);border-radius:max(10px,var(--r));background:rgba(255,255,255,.75)}
.slide.dark .engage{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.2)}
.eg-k{font-size:20px;font-weight:800;letter-spacing:.1em;color:var(--accent);margin-bottom:6px}.eg-p{font-size:32px;font-weight:700;color:inherit;margin-bottom:18px;line-height:1.3}
.opts{display:grid;gap:12px}.opt{position:relative;display:flex;justify-content:space-between;align-items:center;gap:20px;font:inherit;font-size:28px;text-align:inherit;padding:16px 24px;border-radius:12px;border:2px solid var(--hair);background:#fff;color:var(--ink);cursor:pointer;overflow:hidden}
.opt:focus-visible{outline:4px solid var(--accent);outline-offset:3px}.opt[aria-checked=true]{border-color:var(--accent)}
.opt.ok{border-color:#1E7A46;background:#EAF6EF}.opt.no{border-color:#B42318;background:#FDECEA}
.opt .bar{position:absolute;inset-block:0;''' + START + r''':0;width:0;background:rgba(44,95,124,.12);transition:width .3s}.opt .ot,.opt .cnt{position:relative}.opt .cnt{font-weight:800;color:var(--accent)}
.eg-fb{min-height:40px;font-size:27px;margin-top:14px;color:inherit}.eg-reveal{margin-top:10px;font:inherit;font-size:22px;font-weight:700;background:none;border:0;color:var(--accent);cursor:pointer;text-decoration:underline;text-underline-offset:5px}
.eg-ans{display:none;font-size:27px;margin-top:12px}.eg-ans.inline{display:block}.eg-note{font-size:20px;color:var(--mute);margin-top:10px}
.eg-img{max-width:100%;max-height:380px;border-radius:10px;border:1px solid var(--hair)}.eg-link{font-size:26px;margin-top:10px}.eg-link a{color:var(--accent)}
.notes{display:none}.ov{display:none}
[data-step]{opacity:0;transform:translateY(26px);transition:opacity .6s var(--ease),transform .8s var(--ease)}
.slide.in [data-step].on{opacity:1;transform:none}
body.rm [data-step]{transform:none;transition:opacity .15s linear}body.rm .tile{transition:none}
@media (prefers-reduced-motion: reduce){[data-step]{transform:none;transition:opacity .15s linear}.tile,.opt .bar{transition:none}}
.hud{position:fixed;left:0;right:0;bottom:20px;display:flex;justify-content:center;z-index:50;opacity:0;transition:.4s}body.ui .hud,.hud:focus-within{opacity:1}
.hud .box{background:rgba(14,22,32,.82);backdrop-filter:blur(8px);border-radius:999px;padding:8px 16px;color:#cfd8e2;font-size:16px;font-weight:600;display:flex;gap:14px}
.hud button{background:none;border:0;color:#cfd8e2;font:inherit;cursor:pointer}.hud button:hover{color:#fff}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:34vh;overflow:auto;background:rgba(14,22,32,.95);color:#e8eef3;padding:24px 8vw;font-size:24px;line-height:1.5;transform:translateY(100%);transition:.4s;z-index:60;''' + ('direction:rtl' if RTL else '') + r'''}#notes.open{transform:none}
body.overview .slide{cursor:pointer}body.overview .ov{display:block;position:absolute;''' + END + r''':40px;top:20px;font-size:180px;font-weight:800;color:var(--accent2);z-index:9}
@media print{@page{size:1920px 1080px;margin:0}html,body{height:auto;overflow:visible}.vp{position:static}.stage{position:static;transform:none!important;width:1920px;height:auto}.world{position:static;transform:none!important}
.slide{position:relative!important;left:auto!important;top:auto!important;break-after:page;box-shadow:none}[data-step]{opacity:1!important;transform:none!important}.hud,#notes{display:none}
.eg-reveal,.eg-fb,.eg-note,.opt .cnt,.opt .bar{display:none}}
body.pdf [data-step]{opacity:1;transform:none}
</style></head><body class="''' + BODYCLS + r'''">
<div class="vp"><div class="stage" id="stage"><div class="world" id="world">''' + SECTIONS_HTML + r'''</div></div></div>
<div class="hud"><div class="box"><span id="count" dir="ltr"></span><button type="button" data-a="map">Map</button><button type="button" data-a="ov">Overview</button><button type="button" data-a="n">Notes</button><button type="button" data-a="rm" aria-pressed="false">Motion</button><button type="button" data-a="f">Full</button></div></div>
<div id="notes" aria-live="off"></div>
<script>
const ROWS=''' + json.dumps(ROWS) + r''', ORDER=''' + json.dumps(ORDER) + r''', ZOOM=''' + ("true" if ZOOM else "false") + r''', RTL=''' + ("true" if RTL else "false") + r''';
const T=''' + json.dumps({k: S[k] for k in ("correct", "incorrect", "answer")}, ensure_ascii=False) + r''';
const HUB=''' + json.dumps(next((i for i, s in enumerate(slides) if s.get("role") == "agenda"), 0)) + r''';
const SW=1920,SH=1080,GX=520,GY=520,stage=document.getElementById('stage'),world=document.getElementById('world');
const slides=[...document.querySelectorAll('.slide')];
let RM=''' + ("true" if RM_META else "false") + r'''||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
function setRM(v){RM=v;document.body.classList.toggle('rm',RM);const b=document.querySelector('[data-a=rm]');if(b)b.setAttribute('aria-pressed',RM?'true':'false');}
setRM(RM);
const pos=[];let k=0;ROWS.forEach((n,r)=>{for(let c=0;c<n;c++){const idx=ORDER[k++];pos[idx]={x:c*(SW+GX),y:r*(SH+GY)};}});
slides.forEach((s,i)=>{s.style.left=pos[i].x+'px';s.style.top=pos[i].y+'px';const o=s.querySelector('.ov');if(o)o.textContent=String(i+1).padStart(2,'0');const pg=s.querySelector('.runhead .pg');if(pg)pg.textContent=String(i+1).padStart(2,'0');});
function layout(){const f=Math.min(innerWidth/SW,innerHeight/SH);stage.style.transform=`translate(${(innerWidth-SW*f)/2}px,${(innerHeight-SH*f)/2}px) scale(${f})`;}
addEventListener('resize',layout);layout();
const cam={cx:SW/2,cy:SH/2,k:1};function apply(){world.style.transform=`translate(${SW/2-cam.cx*cam.k}px,${SH/2-cam.cy*cam.k}px) scale(${cam.k})`;}
const tgt=i=>({cx:pos[i].x+SW/2,cy:pos[i].y+SH/2,k:1});
let raf=0,fid=0;
function vw(w0,w1,d,rho){const r2=rho*rho,r4=r2*r2;const b0=(w1*w1-w0*w0+r4*d*d)/(2*w0*r2*d),b1=(w1*w1-w0*w0-r4*d*d)/(2*w1*r2*d);const r0=Math.log(Math.sqrt(b0*b0+1)-b0),r1=Math.log(Math.sqrt(b1*b1+1)-b1);const S=(r1-r0)/rho;return{S,f:t=>{const s=t*S,u=(w0/r2)*Math.cosh(r0)*Math.tanh(rho*s+r0)-(w0/r2)*Math.sinh(r0);return{u:u/d,w:w0*Math.cosh(r0)/Math.cosh(rho*s+r0)};}};}
function fly(to,inst){cancelAnimationFrame(raf);const id=++fid,fr={...cam};if(inst||RM){Object.assign(cam,to);apply();return Promise.resolve();}
const w0=SW/fr.k,w1=SW/to.k,dx=to.cx-fr.cx,dy=to.cy-fr.cy,dd=Math.hypot(dx,dy);let S,f;
if(dd<2){const L=Math.log(w1/w0);S=Math.abs(L)/1.35+.001;f=t=>({u:0,w:w0*Math.exp(L*t)});}else{const o=vw(w0,w1,dd,1.35);S=o.S;f=o.f;}
const dur=Math.min(2400,Math.max(1000,S*600)),t0=performance.now();
return new Promise(res=>{const st=now=>{if(id!==fid)return res();let t=Math.min(1,(now-t0)/dur);const e=t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,r=f(e);cam.cx=fr.cx+(dd<2?0:dx*r.u);cam.cy=fr.cy+(dd<2?0:dy*r.u);cam.k=SW/r.w;apply();if(t<1)raf=requestAnimationFrame(st);else{Object.assign(cam,to);apply();res();}};raf=requestAnimationFrame(st);});}
let idx=0,step=0,ov=false;
function setStep(i,s){slides[i].querySelectorAll('[data-step]').forEach(e=>e.classList.toggle('on',+e.dataset.step<=s));step=s;}
function maxStep(i){return +slides[i].dataset.max||0;}
function activate(i){slides.forEach((s,j)=>{s.classList.toggle('in',j===i);s.inert=(j!==i)&&!ov;});document.getElementById('count').textContent=(i+1)+' / '+slides.length;const n=slides[i].querySelector('.notes');document.getElementById('notes').textContent=n?n.textContent:'';}
function go(i,opt){opt=opt||{};i=Math.max(0,Math.min(slides.length-1,i));if(ov){ov=false;document.body.classList.remove('overview');}
if(document.activeElement&&document.activeElement!==document.body&&slides[idx].contains(document.activeElement))document.activeElement.blur();
idx=i;setStep(i,opt.step==='max'?maxStep(i):0);activate(i);fly(tgt(i),opt.inst);}
function next(){if(ov)return;if(step<maxStep(idx))setStep(idx,step+1);else if(idx<slides.length-1)go(idx+1);}
function prev(){if(ov)return;if(step>0)setStep(idx,step-1);else if(idx>0)go(idx-1,{step:'max'});}
function overview(){if(ov){go(idx);return;}ov=true;document.body.classList.add('overview');slides.forEach(s=>{s.classList.add('in');s.inert=false;});
const cols=Math.max(...ROWS),W=cols*SW+(cols-1)*GX,H=ROWS.length*SH+(ROWS.length-1)*GY;fly({cx:W/2,cy:H/2,k:Math.min(SW/(W+300),SH/(H+300))});}
/* quizzes + local polls: real radio buttons, local feedback, no network, keys never leak to the deck */
document.querySelectorAll('.engage').forEach(g=>{const opts=[...g.querySelectorAll('.opt')];if(!opts.length)return;
const fb=g.querySelector('.eg-fb'),mode=g.dataset.mode,corr=g.dataset.correct,counts={};let total=0;
opts.forEach((b,i)=>{b.tabIndex=i?-1:0;});
function choose(b){opts.forEach(o=>{o.setAttribute('aria-checked',o===b?'true':'false');o.tabIndex=o===b?0:-1;});
if(mode==='quiz'){opts.forEach(o=>o.classList.remove('ok','no'));const ok=b.dataset.opt===corr;b.classList.add(ok?'ok':'no');fb.textContent=(ok?T.correct:T.incorrect)+(b.dataset.fb?' '+b.dataset.fb:'');}
else{counts[b.dataset.opt]=(counts[b.dataset.opt]||0)+1;total++;opts.forEach(o=>{const c=counts[o.dataset.opt]||0;o.querySelector('.cnt').textContent=c;o.querySelector('.bar').style.width=(100*c/total)+'%';});}}
opts.forEach((b,i)=>{b.addEventListener('click',e=>{e.stopPropagation();choose(b);});
b.addEventListener('keydown',e=>{const fwd=['ArrowDown',RTL?'ArrowLeft':'ArrowRight'],back=['ArrowUp',RTL?'ArrowRight':'ArrowLeft'];
if(fwd.includes(e.key)||back.includes(e.key)){e.preventDefault();const j=(i+(fwd.includes(e.key)?1:-1)+opts.length)%opts.length;opts[j].focus();}
else if(e.key===' '||e.key==='Enter'){e.preventDefault();choose(b);}e.stopPropagation();});});
const rv=g.querySelector('.eg-reveal');if(rv)rv.addEventListener('click',e=>{e.stopPropagation();const c=opts.find(o=>o.dataset.opt===corr);if(!c)return;opts.forEach(o=>o.classList.remove('no'));c.classList.add('ok');c.focus();fb.textContent=g.querySelector('.eg-ans').textContent;});});
document.addEventListener('click',e=>{const a=e.target.closest('[data-a]');if(a){({map:()=>go(HUB),ov:overview,n:()=>document.getElementById('notes').classList.toggle('open'),rm:()=>setRM(!RM),f:()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()})[a.dataset.a]();return;}
if(e.target.closest('.engage'))return;
if(ov){const s=e.target.closest('.slide');if(s)go(slides.indexOf(s));return;}
const g=e.target.closest('[data-goto]');if(g){go(+g.dataset.goto);return;}});
addEventListener('keydown',e=>{const k=e.key,t=e.target;
if(t&&t.closest&&t.closest('.engage,input,textarea,select,[contenteditable]'))return;      /* interaction owns its keys */
if((k===' '||k==='Enter')&&t&&t.closest&&t.closest('button,a'))return;                       /* let the focused control act */
if([' ','ArrowRight','ArrowDown','PageDown','Enter'].includes(k)){e.preventDefault();next();}else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(k))prev();else if(k==='m'||k==='M')go(HUB);else if(k==='o'||k==='O')overview();else if(k==='n'||k==='N')document.getElementById('notes').classList.toggle('open');else if(k==='r'||k==='R')setRM(!RM);else if(k==='f'||k==='F')document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();else if(k==='Escape'){document.getElementById('notes').classList.remove('open');if(ov)go(idx);}});
let it;addEventListener('mousemove',()=>{document.body.classList.add('ui');clearTimeout(it);it=setTimeout(()=>document.body.classList.remove('ui'),2500);});
(document.fonts?document.fonts.ready:Promise.resolve()).then(()=>go(0,{inst:true}));
window.deck={go,next,prev,overview,setRM,state:()=>({idx,step,RM})};
</script></body></html>'''

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
for w in A.warnings: print("warning:", w)
print("saved", os.path.join(OUT, "index.html"), "| slides:", len(slides), "| rtl:", RTL, "| zoom:", ZOOM, "| system:", d.get("system") or SYS)
