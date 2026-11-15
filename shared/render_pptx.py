# -*- coding: utf-8 -*-
"""blueprint.json -> deck.pptx   (python-pptx)

Covers roles cover/stakes/close/quote/divider/agenda/concept/evidence/process/comparison/
references/appendix and exhibits chart(bar|column|line)/table/diagram(process)/image|screenshot/code.
RTL-correct (sets <a:cs>+lang on every run), dark/light sandwich, generated grid/navy backgrounds,
Morph transitions + Sections when navigation.mode == "zoom".

Usage:  python render_pptx.py blueprint.json out.pptx [assets_dir]
Deps:   python-pptx, Pillow   (LibreOffice/Chrome only needed by render_pdf.py)
"""
import sys, os, json, uuid, io, zipfile, re, shutil, tempfile
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.oxml.ns import qn, nsdecls
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw

BP = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
ASSETS = sys.argv[3] if len(sys.argv) > 3 else os.path.dirname(os.path.abspath(sys.argv[1]))

meta = BP.get("meta", {})
RTL = bool(meta.get("rtl"))
LANG = meta.get("language", "en")
LANGTAG = "he-IL" if LANG == "he" else ("ar-SA" if LANG == "ar" else "en-US")
AL_MAIN = PP_ALIGN.RIGHT if RTL else PP_ALIGN.LEFT

d = BP.get("design", {})
pal = {**{"bg": "FFFFFF", "bgAlt": "F6F7F9", "ink": "1A2230", "mute": "5B6472", "accent": "2C5F7C",
          "accent2": "B4722E", "hair": "E2E5EA", "dark": "1C2A3A"}, **d.get("palette", {})}
def C(k): return RGBColor.from_string(pal[k])
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTE_D = RGBColor(0x9A, 0xA6, 0xB2)
fonts = {**{"display": "Arial", "body": "Arial", "mono": "Courier New"}, **d.get("fonts", {})}
FD, FB, FM = fonts["display"], fonts["body"], fonts["mono"]

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

# ---------- generated backgrounds ----------
_TMP = tempfile.mkdtemp(prefix="psbg_")
def _grid(path, base, minor, major):
    im = Image.new("RGB", (2000, 1125), base); dr = ImageDraw.Draw(im)
    for x in range(0, 2000, 40): dr.line([(x, 0), (x, 1125)], fill=minor)
    for y in range(0, 1125, 40): dr.line([(0, y), (2000, y)], fill=minor)
    for x in range(0, 2000, 200): dr.line([(x, 0), (x, 1125)], fill=major)
    for y in range(0, 1125, 200): dr.line([(0, y), (2000, y)], fill=major)
    im.save(path)
def hx(s): return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
LIGHT_BG = os.path.join(_TMP, "l.png"); _grid(LIGHT_BG, hx(pal["bg"]), (242, 243, 245), (233, 236, 240))
DARK_BG = os.path.join(_TMP, "d.png"); dk = hx(pal["dark"]); _grid(DARK_BG, dk, tuple(min(255, c+5) for c in dk), tuple(min(255, c+10) for c in dk))

def asset_path(ref):
    if not ref: return None
    for a in BP.get("assets", []):
        if a.get("id") == ref and a.get("path"):
            p = a["path"]
            return p if os.path.isabs(p) else os.path.join(ASSETS, p)
    p = ref if os.path.isabs(ref) else os.path.join(ASSETS, ref)
    return p if os.path.exists(p) else None

# ---------- text helpers (RTL-correct) ----------
def _rtl(p, align):
    p._p.get_or_add_pPr().set('rtl', '1' if RTL else '0'); p.alignment = align
def _cs(r, font):
    rPr = r._r.get_or_add_rPr(); latin = rPr.find(qn('a:latin')); prev = latin
    for tag in ('a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {}); (prev.addnext(el) if prev is not None else rPr.append(el))
        el.set('typeface', font); prev = el
    rPr.set('lang', LANGTAG); rPr.set('altLang', 'en-US')
def tb(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP, name=None):
    sh = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name: sh.name = name
    tf = sh.text_frame; tf.word_wrap = True
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"): setattr(tf, m, 0)
    tf.vertical_anchor = anchor; return tf
def run(p, text, size, color, bold=False, font=None, italic=False):
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.name = font or FB; r.font.color.rgb = color; _cs(r, font or FB); return r
def para(tf, text, size=16, color=None, bold=False, align=None, font=None, italic=False,
         sb=0, sa=6, line=None, first=False):
    p = tf.paragraphs[0] if (first and not tf.paragraphs[0].runs) else tf.add_paragraph()
    run(p, text, size, color if color is not None else C("ink"), bold, font, italic)
    p.space_before, p.space_after = Pt(sb), Pt(sa)
    if line: p.line_spacing = line
    _rtl(p, align if align is not None else AL_MAIN); return p
def runs_para(tf, parts, size=16, align=None, sb=0, sa=6, line=None, first=False):
    p = tf.paragraphs[0] if (first and not tf.paragraphs[0].runs) else tf.add_paragraph()
    for t, ov in parts:
        run(p, t, ov.get("size", size), ov.get("color", C("ink")), ov.get("bold", False),
            ov.get("font"), ov.get("italic", False))
    p.space_before, p.space_after = Pt(sb), Pt(sa)
    if line: p.line_spacing = line
    _rtl(p, align if align is not None else AL_MAIN); return p

SHADOW = ('<a:effectLst %s><a:outerShdw blurRad="90000" dist="30000" dir="5400000" rotWithShape="0">'
          '<a:srgbClr val="1A2230"><a:alpha val="18000"/></a:srgbClr></a:outerShdw></a:effectLst>') % nsdecls('a')
def rrect(slide, x, y, w, h, fill=None, line=None, rad=0.045, shadow=True, name=None):
    sp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if name: sp.name = name
    sp.fill.solid(); sp.fill.fore_color.rgb = fill if fill is not None else WHITE
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(1)
    try: sp.adjustments[0] = rad
    except Exception: pass
    sp.shadow.inherit = False
    if shadow: sp._element.spPr.append(parse_xml(SHADOW))
    return sp
def fitted(slide, img, bx, by, bw, bh):
    iw, ih = Image.open(img).size; ar = iw/ih; bar = bw/bh
    w, h = (bw, bw/ar) if ar > bar else (bh*ar, bh)
    slide.shapes.add_picture(img, Inches(bx+(bw-w)/2), Inches(by+(bh-h)/2), Inches(w), Inches(h))

def bg(slide, dark=False, photo=None):
    p = asset_path(photo) if photo else None
    slide.shapes.add_picture(p or (DARK_BG if dark else LIGHT_BG), 0, 0, SW, SH)
    if p and dark:  # navy scrim over photo for text legibility
        sc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
        sc.fill.solid(); sc.fill.fore_color.rgb = C("dark"); sc.line.fill.background(); sc.shadow.inherit = False
        sc.fill.transparency = 0  # python-pptx can't set fill alpha directly; approximate with solid dark on dark photo
        sc._element.spPr.append(parse_xml('<a:alphaModFix %s amt="62000"/>' % nsdecls('a')))

def new(dark=False, photo=None):
    s = prs.slides.add_slide(BLANK); bg(s, dark, photo); return s

# ---------- header ----------
def header(slide, kicker, title, dark=False, size=30):
    tcol = WHITE if dark else C("ink"); kcol = MUTE_D if dark else C("accent")
    if kicker:
        para(tb(slide, 0.65, 0.42, 12.03, 0.4, name="!!kicker"), kicker, 13.5, kcol, True, AL_MAIN, FB, sa=0, first=True)
    if title:
        para(tb(slide, 0.65, 0.82, 12.03, 1.2, name="!!title"), title, size, tcol, True, AL_MAIN, FD, sa=0, line=1.03, first=True)

# ---------- exhibits ----------
TX_X, TX_W, CD_X, CD_W = (6.95, 5.73, 0.65, 5.95)
def ex_image(slide, path, x, y, w, h, caption):
    rrect(slide, x, y, w, h, WHITE, C("hair"))
    ch = 0.34 if caption else 0
    fitted(slide, path, x+0.14, y+0.14, w-0.28, h-0.28-ch)
    if caption:
        para(tb(slide, x+0.14, y+h-ch-0.02, w-0.28, ch, MSO_ANCHOR.MIDDLE), caption, 10.5, C("mute"), align=AL_MAIN, sa=0, first=True)
def ex_chart(slide, data, x, y, w, h):
    cd = CategoryChartData(); cats = data.get("categories", [])
    cd.categories = cats
    for s in data.get("series", []): cd.add_series(s.get("name", ""), s.get("values", []))
    kind = {"bar": XL_CHART_TYPE.BAR_CLUSTERED, "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
            "line": XL_CHART_TYPE.LINE}.get(data.get("kind", "column"), XL_CHART_TYPE.COLUMN_CLUSTERED)
    gf = slide.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart; ch.has_title = False
    ch.has_legend = len(data.get("series", [])) > 1
    if ch.has_legend: ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
    try:
        pl = ch.plots[0]; pl.has_data_labels = True; pl.data_labels.number_format = '0'; pl.data_labels.number_format_is_linked = False
        for i, s in enumerate(ch.series):
            s.format.fill.solid(); s.format.fill.fore_color.rgb = C("accent") if i == 0 else C("mute")
    except Exception: pass
def ex_table(slide, data, x, y, w, h):
    cols = data.get("columns", []); rows = data.get("rows", [])
    disp_cols = list(reversed(cols)) if RTL else cols
    n, m = len(rows)+1, len(cols)
    gt = slide.shapes.add_table(n, m, Inches(x), Inches(y), Inches(w), Inches(h)).table
    gt.first_row = False; gt.horz_banding = False
    for ri in range(n):
        src = disp_cols if ri == 0 else (list(reversed(rows[ri-1])) if RTL else rows[ri-1])
        for ci in range(m):
            c = gt.cell(ri, ci); c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.fill.solid(); c.fill.fore_color.rgb = C("dark") if ri == 0 else (WHITE if ri % 2 else C("bgAlt"))
            p = c.text_frame.paragraphs[0]
            run(p, str(src[ci]), 12.5, WHITE if ri == 0 else C("ink"), ri == 0 or ci == (m-1 if RTL else 0), FB)
            _rtl(p, AL_MAIN)
def ex_diagram(slide, data, x, y, w, h):
    steps = data.get("steps", []); n = len(steps) or 1
    gap = 0.18; cw = (w - gap*(n-1))/n
    for i, st in enumerate(steps):
        xi = x + (n-1-i)*(cw+gap) if RTL else x + i*(cw+gap)
        last = i == n-1
        rrect(slide, xi, y, cw, h, C("dark") if last else WHITE, None if last else C("hair"))
        t = tb(slide, xi+0.08, y+0.12, cw-0.16, h-0.24, MSO_ANCHOR.MIDDLE)
        para(t, "%02d" % (i+1), 14, (MUTE_D if last else C("accent")), True, PP_ALIGN.CENTER, FM, sa=4, first=True)
        para(t, st, 14, (WHITE if last else C("ink")), True, PP_ALIGN.CENTER, FB, sa=0, line=1.05)
def ex_code(slide, text, x, y, w, h, caption):
    rrect(slide, x, y, w, h, C("dark"), None)
    t = tb(slide, x+0.3, y+0.25, w-0.6, h-0.5)
    for ln in str(text).splitlines() or [""]:
        para(t, ln, 15, WHITE, font=FM, align=PP_ALIGN.LEFT, sa=2, first=(t.paragraphs[0].runs == []))

def place_exhibit(slide, ex, box):
    x, y, w, h = box; t = ex.get("type"); cap = ex.get("caption", "")
    if t in ("screenshot", "image"):
        p = asset_path(ex.get("ref"))
        if p: ex_image(slide, p, x, y, w, h, cap)
        else: para(tb(slide, x, y, w, h, MSO_ANCHOR.MIDDLE), "[%s]" % (ex.get("ref") or "image"), 14, C("mute"), align=PP_ALIGN.CENTER, first=True)
    elif t == "chart": ex_chart(slide, ex.get("data", {}), x, y, w, h)
    elif t == "table": ex_table(slide, ex.get("data", {}), x, y, w, h)
    elif t == "diagram": ex_diagram(slide, ex.get("data", {}), x, y, w, min(h, 1.9))
    elif t == "code": ex_code(slide, ex.get("data", ""), x, y, w, h, cap)

# ---------- slide renderers by role ----------
def statement(sl, title, bullets, dark=True, big=None):
    tf = tb(sl, 0.9, 2.4, 11.5, 2.6, MSO_ANCHOR.MIDDLE)
    if big: para(tf, big, 140, C("accent2"), True, AL_MAIN, FD, sa=10, first=True)
    para(tf, title or "", 34, WHITE if dark else C("ink"), True, AL_MAIN, FD, sa=12, line=1.1, first=(big is None))
    for b in bullets or []:
        para(tf, b.get("text", ""), 18, MUTE_D if dark else C("mute"), align=AL_MAIN, italic=True, sa=6)

def render(sl_data):
    role = sl_data.get("role", "concept")
    dark = sl_data.get("dark", role in ("cover", "stakes", "close", "quote", "divider"))
    bgk = (sl_data.get("background") or {})
    photo = bgk.get("photo")
    s = new(dark=dark, photo=photo)
    title = sl_data.get("actionTitle", ""); kicker = sl_data.get("kicker", "")
    bullets = sl_data.get("bullets", []); ex = sl_data.get("exhibit")

    if role == "cover":
        tf = tb(s, 0.9, 2.1, 11.5, 2.4)
        if kicker: para(tf, kicker, 20, MUTE_D, True, AL_MAIN, FB, sa=10, first=True)
        para(tf, title or meta.get("title", ""), 54, WHITE, True, AL_MAIN, FD, sa=6, line=1.0, first=(not kicker))
        if meta.get("subtitle"): para(tf, meta["subtitle"], 20, MUTE_D, align=AL_MAIN, sa=0)
        foot = tb(s, 0.9, 6.3, 11.5, 0.8)
        if meta.get("authors"): para(foot, "  ·  ".join(meta["authors"]), 16, C("accent"), True, AL_MAIN, FB, sa=2, first=True)
        line2 = "   ·   ".join([x for x in [meta.get("event"), meta.get("date")] if x])
        if line2: para(foot, line2, 12.5, MUTE_D, align=AL_MAIN, font=FM, sa=0)
    elif role in ("stakes", "close", "quote", "divider"):
        statement(s, title, bullets, dark=True)
    elif role == "agenda":
        header(s, kicker, title, dark=dark)
        secs = BP.get("sections", []); n = max(1, len(secs)); gap = 0.4; cw = (12.03-gap*(n-1))/n
        for i, sec in enumerate(secs):
            xi = 0.65 + (n-1-i)*(cw+gap) if RTL else 0.65 + i*(cw+gap)
            rrect(s, xi, 2.6, cw, 3.2, C("dark") if dark else WHITE, None if dark else C("hair"))
            t = tb(s, xi+0.3, 3.0, cw-0.6, 2.4)
            para(t, "%02d" % (i+1), 40, C("accent2"), True, AL_MAIN, FD, sa=8, first=True)
            para(t, sec.get("title", ""), 24, WHITE if dark else C("ink"), True, AL_MAIN, FD, sa=0)
    elif role in ("evidence", "comparison", "process") and ex:
        header(s, kicker, title, dark=dark)
        side = ex.get("side", "left")
        if role == "process" or ex.get("type") == "diagram":
            place_exhibit(s, ex, (0.65, 3.0, 12.03, 1.9))
            if ex.get("caption"): para(tb(s, 0.65, 5.2, 12.03, 0.5), ex["caption"], 14, C("mute"), align=AL_MAIN, italic=True, sa=0, first=True)
            for i, b in enumerate(bullets or []):
                para(tb(s, 0.65, 5.7+i*0.0, 12.03, 0.5), b.get("text", ""), 16, C("mute"), align=AL_MAIN, sa=4, first=True)
        elif role == "comparison" or ex.get("type") == "table":
            place_exhibit(s, ex, (0.9, 2.5, 11.5, 3.6))
            for b in bullets or []:
                para(tb(s, 0.65, 6.3, 12.03, 0.5), b.get("text", ""), 15, C("mute"), align=AL_MAIN, italic=True, sa=0, first=True)
        else:
            cx = CD_X if side == "left" else TX_X; tx = TX_X if side == "left" else CD_X
            place_exhibit(s, ex, (cx, 2.05, CD_W, 4.6))
            tf = tb(s, tx, 2.3, TX_W, 4.2)
            first = True
            for b in bullets or []:
                parts = [("▪  ", {"color": C("accent"), "bold": True, "size": 13})]
                if b.get("lead"): parts.append((b["lead"]+"  ", {"color": C("ink"), "bold": True, "size": 16}))
                parts.append((b.get("text", ""), {"color": C("mute"), "size": 16}))
                runs_para(tf, parts, align=AL_MAIN, sa=12, line=1.15, first=first); first = False
    elif role in ("references", "appendix"):
        header(s, kicker, title or ("References" if role == "references" else "Appendix"), dark=dark)
        tf = tb(s, 0.65, 2.1, 12.03, 4.8)
        for b in bullets or []:
            para(tf, b.get("text", ""), 15, C("mute"), align=AL_MAIN, sa=8, first=(tf.paragraphs[0].runs == []))
    else:  # concept / default
        header(s, kicker, title, dark=dark)
        if ex: place_exhibit(s, ex, (CD_X, 2.05, CD_W, 4.6))
        tf = tb(s, (TX_X if ex else 0.65), 2.3, (TX_W if ex else 12.03), 4.2)
        first = True
        for b in bullets or []:
            parts = [("▪  ", {"color": C("accent"), "bold": True, "size": 13})]
            if b.get("lead"): parts.append((b["lead"]+"  ", {"color": C("ink"), "bold": True, "size": 17}))
            parts.append((b.get("text", ""), {"color": C("mute"), "size": 17}))
            runs_para(tf, parts, align=AL_MAIN, sa=12, line=1.2, first=first); first = False

    if sl_data.get("speakerNotes"):
        s.notes_slide.notes_text_frame.text = sl_data["speakerNotes"]
    return s

for sl in BP.get("slides", []):
    render(sl)

# ---------- names, Morph, Sections ----------
ZOOM = (BP.get("navigation", {}).get("mode") == "zoom")
MORPH = ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
         'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
         '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
         '<p:transition spd="slow" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" p14:dur="1400">'
         '<p159:morph option="byObject"/></p:transition></mc:Choice>'
         '<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')
for si, (sl, data) in enumerate(zip(prs.slides, BP.get("slides", [])), 1):
    for k, sh in enumerate(sl.shapes):
        if not sh.name.startswith("!!"): sh.name = "s%d_%d" % (si, k)
    if (data.get("animation", {}).get("transition") == "morph") or (ZOOM and si > 1):
        el = parse_xml(MORPH); clr = sl._element.find(qn('p:clrMapOvr'))
        (clr.addnext(el) if clr is not None else sl._element.cSld.addnext(el))

if ZOOM and BP.get("sections"):
    idx = {s["id"]: i for i, s in enumerate(BP["slides"])}
    sldIds = [c.get('id') for c in prs.slides._sldIdLst]
    secs = ""
    for sec in BP["sections"]:
        ids = "".join('<p14:sldId id="%s"/>' % sldIds[idx[sid]] for sid in sec.get("slideIds", []) if sid in idx)
        if not ids: continue
        secs += '<p14:section name="%s" id="{%s}"><p14:sldIdLst>%s</p14:sldIdLst></p14:section>' % (sec["title"], str(uuid.uuid4()).upper(), ids)
    if secs:
        prs.part._element.append(parse_xml(
            '<p:extLst xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            '<p:ext uri="{521415D9-36F7-43E2-AB2F-B90AF26B5E84}">'
            '<p14:sectionLst xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">'
            + secs + '</p14:sectionLst></p:ext></p:extLst>'))

prs.save(OUT)

# ---------- theme fonts -> deck font for latin/ea/cs ----------
tmp = OUT + ".tmp"
with zipfile.ZipFile(OUT) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename.startswith("ppt/theme/") and it.filename.endswith(".xml"):
            x = data.decode("utf-8")
            def fix(m):
                blk = m.group(0)
                for tag in ("latin", "ea", "cs"): blk = re.sub(r'<a:%s typeface="[^"]*"' % tag, '<a:%s typeface="%s"' % (tag, FB), blk)
                return blk
            data = re.sub(r'<a:(majorFont|minorFont)>.*?</a:\1>', fix, x, flags=re.S).encode("utf-8")
        zout.writestr(it, data)
shutil.move(tmp, OUT)
shutil.rmtree(_TMP, ignore_errors=True)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst), "| rtl:", RTL, "| zoom:", ZOOM)
