# -*- coding: utf-8 -*-
"""blueprint.json -> deck.pptx   (python-pptx)

Roles cover/stakes/close/quote/divider/agenda/concept/evidence/process/comparison/references/appendix,
layouts statement/split/full-exhibit/big-number, design-system tokens (type scale, motif, exhibit
frame, margins). Exhibits: native editable charts (column/bar/line/scatter, units + axis titles +
number formats from the same spec as HTML), tables, diagrams (chain/timeline/sequence as shapes),
images (SVG via raster fallbackPath), code. Quizzes: option shapes hyperlink to an answer slide.
Citations in the slide foot, generated sources/credits slides with links, alt text on pictures.
RTL-correct (sets <a:cs>+lang on every run), Morph transitions + Sections when navigation.mode=="zoom".

Usage:  python render_pptx.py blueprint.json out.pptx [assets_dir]
Deps:   python-pptx, Pillow   (LibreOffice/Chrome only needed by render_pdf.py)
"""
import sys, os, uuid, zipfile, re, shutil, tempfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.chart.data import CategoryChartData, XyChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_MARKER_STYLE
from pptx.oxml.ns import qn, nsdecls
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import blueprint_lib as bl  # noqa: E402

BP = bl.load(sys.argv[1])
OUT = sys.argv[2]
ASSETS = sys.argv[3] if len(sys.argv) > 3 else os.path.dirname(os.path.abspath(sys.argv[1]))

meta = BP.get("meta", {})
RTL = bool(meta.get("rtl"))
LANG = meta.get("language", "en")
LANGTAG = {"he": "he-IL", "ar": "ar-SA", "fa": "fa-IR"}.get(LANG.split("-")[0], "en-US")
AL_MAIN = PP_ALIGN.RIGHT if RTL else PP_ALIGN.LEFT
S = bl.strings(LANG)

d = BP.get("design", {})
SYS, TOK = bl.resolve_system(d)
pal = bl.palette(d)
def C(k): return RGBColor.from_string(pal[k])
def RGB(h): return RGBColor.from_string(h)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTE_D = RGBColor(0x9A, 0xA6, 0xB2)
fonts = {**{"display": "Arial", "body": "Arial", "mono": "Courier New"}, **d.get("fonts", {})}
FD, FB, FM = fonts["display"], fonts["body"], fonts["mono"]
A = bl.Assets(BP, ASSETS)
SLIDES = bl.expand_slides(BP, "pptx")
SECTIONS = BP.get("sections", [])

MG = TOK["margin"] / 144.0                       # tokens are px at 1920; 144 px = 1 in
CW = 13.333 - 2 * MG                             # content width
TS, BOLDT, BS = TOK["titleScale"], TOK["titleWeight"] >= 700, TOK["bodyScale"]
LIGHT = pal[TOK["lightBg"]] if TOK["lightBg"] in pal else pal["bg"]
FRAME = TOK["frame"]

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

# ---------- generated backgrounds ----------
_TMP = tempfile.mkdtemp(prefix="psbg_")
def hx(s): return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
def _grid(path, base, minor, major):
    im = Image.new("RGB", (2000, 1125), base); dr = ImageDraw.Draw(im)
    for x in range(0, 2000, 40): dr.line([(x, 0), (x, 1125)], fill=minor)
    for y in range(0, 1125, 40): dr.line([(0, y), (2000, y)], fill=minor)
    for x in range(0, 2000, 200): dr.line([(x, 0), (x, 1125)], fill=major)
    for y in range(0, 1125, 200): dr.line([(0, y), (2000, y)], fill=major)
    im.save(path)
LIGHT_BG = os.path.join(_TMP, "l.png"); lb = hx(LIGHT)
_grid(LIGHT_BG, lb, tuple(max(0, c - 13) for c in lb), tuple(max(0, c - 22) for c in lb))
DARK_BG = os.path.join(_TMP, "d.png"); dk = hx(pal["dark"]); _grid(DARK_BG, dk, tuple(min(255, c+5) for c in dk), tuple(min(255, c+10) for c in dk))

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
def run(p, text, size, color, bold=False, font=None, italic=False, url=None):
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.name = font or FB; r.font.color.rgb = color; _cs(r, font or FB)
    if url and bl.is_safe_url(url): r.hyperlink.address = url
    return r
def para(tf, text, size=16, color=None, bold=False, align=None, font=None, italic=False,
         sb=0, sa=6, line=None, first=False, url=None):
    p = tf.paragraphs[0] if (first and not tf.paragraphs[0].runs) else tf.add_paragraph()
    run(p, text, size, color if color is not None else C("ink"), bold, font, italic, url)
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
def rrect(slide, x, y, w, h, fill=None, line=None, rad=0.045, shadow=True, name=None, shape=None):
    shape = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if rad else MSO_SHAPE.RECTANGLE)
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if name: sp.name = name
    if fill is False: sp.fill.background()
    else: sp.fill.solid(); sp.fill.fore_color.rgb = fill if fill is not None else WHITE
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(1)
    if rad and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try: sp.adjustments[0] = rad
        except Exception: pass
    sp.shadow.inherit = False
    if shadow: sp._element.spPr.append(parse_xml(SHADOW))
    return sp
def frame_box(slide, x, y, w, h):
    """Exhibit frame per the design system's `frame` token."""
    if FRAME == "card": return rrect(slide, x, y, w, h, WHITE, C("hair"), rad=min(0.08, TOK["radius"] / 400.0))
    if FRAME == "hairline": return rrect(slide, x, y, w, h, WHITE, C("hair"), rad=0, shadow=False)
    return None
def set_alt(pic, alt):
    if alt: pic._element.nvPicPr.cNvPr.set("descr", alt)
def fitted(slide, img, bx, by, bw, bh, alt="", cover=False):
    iw, ih = Image.open(img).size; ar = iw/ih; bar = bw/bh
    if cover:
        pic = slide.shapes.add_picture(img, Inches(bx), Inches(by), Inches(bw), Inches(bh))
        if ar > bar: c = (1 - bar/ar) / 2; pic.crop_left = pic.crop_right = c
        else: c = (1 - ar/bar) / 2; pic.crop_top = pic.crop_bottom = c
    else:
        w, h = (bw, bw/ar) if ar > bar else (bh*ar, bh)
        pic = slide.shapes.add_picture(img, Inches(bx+(bw-w)/2), Inches(by+(bh-h)/2), Inches(w), Inches(h))
    set_alt(pic, alt); return pic
def alpha_fill(shape, hexcol, alpha_pct):
    shape.fill.solid(); shape.fill.fore_color.rgb = RGB(hexcol)
    clr = shape.fill._xPr.find(qn('a:solidFill'))[0]
    clr.append(parse_xml('<a:alpha %s val="%d"/>' % (nsdecls('a'), int(alpha_pct * 1000))))

def bg(slide, dark=False, photo=None):
    p = A.file_for(photo, raster_only=True) if photo else None
    if p:
        fitted(slide, p, 0, 0, 13.333, 7.5, cover=True, alt=A.alt(photo, ""))
        sc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH); sc.line.fill.background(); sc.shadow.inherit = False
        alpha_fill(sc, pal["dark"], 62 if dark else 30)
    elif dark:
        if TOK["motif"] == "grid": slide.shapes.add_picture(DARK_BG, 0, 0, SW, SH)
        else: slide.background.fill.solid(); slide.background.fill.fore_color.rgb = C("dark")
    else:
        if TOK["motif"] == "grid": slide.shapes.add_picture(LIGHT_BG, 0, 0, SW, SH)
        else: slide.background.fill.solid(); slide.background.fill.fore_color.rgb = RGB(LIGHT)

def sec_index(sl):
    for i, s in enumerate(SECTIONS):
        if sl.get("section") == s.get("id") or sl.get("id") in (s.get("slideIds") or []): return i + 1
    return None

def motif(slide, sl, dark, n):
    role = sl.get("role")
    si = sec_index(sl)
    if dark or role == "cover": return
    if TOK["motif"] == "rule":
        st = SECTIONS[si-1].get("title", "") if si else ""
        t = tb(slide, MG, 0.22, CW, 0.3)
        p = para(t, meta.get("title", "") + ((" · " + st) if st else ""), 9.5, C("mute"), first=True, sa=0)
        tn = tb(slide, MG, 0.22, CW, 0.3); para(tn, "%02d" % n, 9.5, C("mute"), align=PP_ALIGN.LEFT if RTL else PP_ALIGN.RIGHT, first=True, sa=0)
        ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(MG), Inches(0.55), Inches(MG + CW), Inches(0.55))
        ln.line.color.rgb = C("hair"); ln.line.width = Pt(0.75)
    if TOK["motif"] == "numbers" and si and role not in ("references", "appendix"):
        x = 0.25 if RTL else 13.333 - 0.25 - 2.6
        t = tb(slide, x, 0.0, 2.6, 1.7, name="!!secnum")
        para(t, "%02d" % si, 110, C("hair"), True, PP_ALIGN.LEFT if RTL else PP_ALIGN.RIGHT, FD, first=True, sa=0, line=0.9)

# ---------- header ----------
def kicker_text(sl, kicker):
    if TOK["kicker"] == "number" and sec_index(sl):
        return "%02d%s" % (sec_index(sl), (" — " + kicker) if kicker else "")
    return kicker
def header(slide, sl, kicker, title, dark=False, size=30, x=None, w=None, y0=None):
    x = MG if x is None else x; w = CW if w is None else w
    y0 = (0.62 if TOK["motif"] == "rule" else 0.42) if y0 is None else y0
    if TOK["motif"] == "numbers" and sec_index(sl) and not dark:   # keep the title clear of the section numeral
        nx0, nx1 = (0.25, 2.85) if RTL else (13.333 - 2.85, 13.333 - 0.25)
        if x < nx1 and x + w > nx0:
            if RTL: cut = max(0.0, nx1 - x); x += cut; w -= cut
            else: w -= max(0.0, x + w - nx0)
    tcol = WHITE if dark else C("ink"); kcol = MUTE_D if dark else (C("mute") if TOK["kicker"] == "caps" else C("accent"))
    k = kicker_text(sl, kicker)
    if k:
        para(tb(slide, x, y0, w, 0.4, name="!!kicker"), k, 12.5 if TOK["kicker"] == "caps" else 13.5, kcol, True, AL_MAIN, FB, sa=0, first=True)
    if title:
        sz = max(22, size * TS * bl.title_scale_for(title))
        para(tb(slide, x, y0 + 0.4, w, 1.3, name="!!title"), title, sz, tcol, BOLDT, AL_MAIN, FD, sa=0, line=1.03, first=True)

def footer(slide, sl, dark):
    f = bl.slide_footer(BP, sl, bl.slide_asset_ids(sl))
    if f and sl.get("role") != "references":
        para(tb(slide, MG, 6.98, CW, 0.32, MSO_ANCHOR.BOTTOM), f, 9.5, MUTE_D if dark else C("mute"), first=True, sa=0)

# ---------- exhibits ----------
SER_HEX, HL_HEX, BASE1_HEX = bl.chart_colors(pal)   # same inks as the HTML chart (distinct even when accent == accent2)
def ex_image(slide, ref, x, y, w, h, caption, alt="", bleed=False):
    path = A.file_for(ref, raster_only=True)
    if not path:
        rrect(slide, x, y, w, h, C("bgAlt"), C("hair"), rad=0, shadow=False)
        para(tb(slide, x, y, w, h, MSO_ANCHOR.MIDDLE), "[%s]" % (alt or ref or "image"), 14, C("mute"), align=PP_ALIGN.CENTER, first=True)
        return
    alt = alt or A.alt(ref, caption)
    if bleed:
        fitted(slide, path, x, y, w, h, alt, cover=True); return
    fb = frame_box(slide, x, y, w, h); pad = 0.14 if fb is not None else 0
    ch = 0.34 if caption else 0
    fitted(slide, path, x+pad, y+pad, w-2*pad, h-2*pad-ch, alt)
    if caption:
        para(tb(slide, x+pad, y+h-ch-0.02, w-2*pad, ch, MSO_ANCHOR.MIDDLE), caption, 10.5, C("mute"), align=AL_MAIN, sa=0, first=True)
def ex_chart(slide, data, x, y, w, h):
    sp = bl.chart_spec(data)
    if sp["kind"] == "unsupported":
        ex_table(slide, bl.table_from_chart(sp), x, y, w, h * 0.8); return
    dec, unit = sp["decimals"], sp["unit"]
    if sp["kind"] == "scatter":
        cd = XyChartData()
        for s in sp["series"]:
            ser = cd.add_series(s["name"])
            for p in s["points"]: ser.add_data_point(p[0], p[1])
        kind = XL_CHART_TYPE.XY_SCATTER
    else:
        cd = CategoryChartData(number_format=bl.excel_format(dec, ""))
        cd.categories = sp["categories"]
        for s in sp["series"]: cd.add_series(s["name"], s["values"])
        kind = {"bar": XL_CHART_TYPE.BAR_CLUSTERED, "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
                "line": XL_CHART_TYPE.LINE_MARKERS}[sp["kind"]]
    gf = slide.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart; ch.font.size = Pt(12); ch.font.name = FB; ch.font.color.rgb = C("mute")
    ch.has_title = bool(sp["title"])
    if sp["title"]: ch.chart_title.text_frame.text = sp["title"]
    ch.has_legend = len(sp["series"]) > 1
    if ch.has_legend: ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
    va, ca = ch.value_axis, ch.category_axis
    va.has_major_gridlines = True; va.major_gridlines.format.line.color.rgb = C("hair")
    va.format.line.fill.background()
    va.tick_labels.number_format = "General"; va.tick_labels.number_format_is_linked = False
    if sp["kind"] in ("column", "bar", "line"):
        allv0 = [v for s in sp["series"] for v in s["values"]] or [0]
        base0 = sp["yMin"] if (sp["kind"] == "line" and sp["yMin"] is not None) else min(0, min(allv0))
        lo, hi, stp = bl.nice_ticks(max(allv0), base0); va.maximum_scale = hi; va.major_unit = stp
    allv = [v for s in sp["series"] for v in s["values"]] or [0]
    if sp["kind"] in ("column", "bar"): va.minimum_scale = min(0, min(allv))
    elif sp["kind"] == "line": va.minimum_scale = sp["yMin"] if sp["yMin"] is not None else min(0, min(allv))
    if sp["kind"] == "bar": ca.reverse_order = True    # first category on top, like the HTML chart
    yl = sp["yLabel"] or unit
    if yl: va.has_title = True; va.axis_title.text_frame.text = yl
    if sp["xLabel"]: ca.has_title = True; ca.axis_title.text_frame.text = sp["xLabel"]
    pl = ch.plots[0]
    if sp["kind"] in ("column", "bar"):
        pl.has_data_labels = True; dl = pl.data_labels
        dl.number_format = bl.excel_format(dec, unit, RTL); dl.number_format_is_linked = False
        dl.font.size = Pt(13); dl.font.bold = True; dl.font.color.rgb = C("ink")
        try: pl.gap_width = 60
        except Exception: pass
    for i, s in enumerate(ch.series):
        single_hl = sp["kind"] in ("column", "bar") and len(sp["series"]) == 1 and sp["highlight"] is not None
        col = RGBColor.from_string(BASE1_HEX if single_hl else SER_HEX[i % 4])
        if sp["kind"] == "line":
            s.format.line.color.rgb = col; s.format.line.width = Pt(3); s.smooth = False
            s.marker.style = XL_MARKER_STYLE.CIRCLE; s.marker.size = 7
            s.marker.format.fill.solid(); s.marker.format.fill.fore_color.rgb = col; s.marker.format.line.color.rgb = col
            vals = sp["series"][i]["values"]
            for j in {len(vals) - 1} | ({sp["highlight"]} if sp["highlight"] is not None else set()):
                if 0 <= j < len(vals):
                    lab = s.points[j].data_label; lab.has_text_frame = True; lab.position = XL_LABEL_POSITION.ABOVE
                    lab.text_frame.text = bl.ltr(bl.fmt_num(vals[j], dec, unit), RTL)
                    r = lab.text_frame.paragraphs[0].runs[0]; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C("ink")
        elif sp["kind"] == "scatter":
            s.marker.style = XL_MARKER_STYLE.CIRCLE; s.marker.size = 10
            s.marker.format.fill.solid(); s.marker.format.fill.fore_color.rgb = col; s.format.line.fill.background()
        else:
            s.format.fill.solid(); s.format.fill.fore_color.rgb = col
            if len(sp["series"]) == 1 and sp["highlight"] is not None and sp["highlight"] < len(sp["categories"]):
                pt = s.points[sp["highlight"]]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = RGBColor.from_string(HL_HEX)
    return gf
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
def ex_chain(slide, data, x, y, w, h):
    steps = data.get("steps", []); n = len(steps) or 1
    gap = 0.18; cw = (w - gap*(n-1))/n
    for i, st in enumerate(steps):
        xi = x + (n-1-i)*(cw+gap) if RTL else x + i*(cw+gap)
        last = i == n-1
        rrect(slide, xi, y, cw, h, C("dark") if last else WHITE, None if last else C("hair"), rad=min(0.08, TOK["radius"] / 300.0), shadow=FRAME == "card")
        t = tb(slide, xi+0.08, y+0.12, cw-0.16, h-0.24, MSO_ANCHOR.MIDDLE)
        para(t, "%02d" % (i+1), 14, (MUTE_D if last else C("accent")), True, PP_ALIGN.CENTER, FM, sa=4, first=True)
        para(t, st, 14, (WHITE if last else C("ink")), True, PP_ALIGN.CENTER, FB, sa=0, line=1.05)
def ex_timeline(slide, data, x, y, w, h):
    evs = data.get("events") or [{"label": s} for s in data.get("steps", [])]; n = max(len(evs), 1)
    cw = w / n; ly = y + 0.3
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(ly), Inches(x + w), Inches(ly))
    ln.line.color.rgb = C("hair"); ln.line.width = Pt(2.5)
    for i, e in enumerate(evs):
        xi = x + (n-1-i)*cw if RTL else x + i*cw
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(xi + 0.05), Inches(ly - 0.14), Inches(0.28), Inches(0.28))
        dot.fill.solid(); dot.fill.fore_color.rgb = C("accent2" if i == n-1 else "accent"); dot.line.fill.background(); dot.shadow.inherit = False
        t = tb(slide, xi, ly + 0.3, cw - 0.15, h - 0.6)
        if e.get("when"): para(t, str(e["when"]), 15, C("accent"), True, first=True, sa=2)
        para(t, str(e.get("label", "")), 14, C("ink"), first=not e.get("when"), sa=0, line=1.1)
def _arrow(conn):
    ln = conn.line._get_or_add_ln(); ln.append(parse_xml('<a:tailEnd %s type="triangle" w="med" len="med"/>' % nsdecls('a')))
def ex_sequence(slide, data, x, y, w, h):
    actors = data.get("actors", []); msgs = data.get("messages", []); n = max(len(actors), 1)
    bw = 1.9; xs = {}
    for i, a in enumerate(actors):
        cx = x + bw/2 + (w - bw) * (i / max(n - 1, 1))
        xs[a] = (x + w - (cx - x)) if RTL else cx
    step = min(0.62, (h - 0.8) / max(len(msgs), 1)); bottom = y + 0.6 + step * len(msgs) + 0.2
    for a, cx in xs.items():
        b = rrect(slide, cx - bw/2, y, bw, 0.5, C("dark"), None, rad=0.1, shadow=False)
        t = tb(slide, cx - bw/2, y, bw, 0.5, MSO_ANCHOR.MIDDLE); para(t, a, 14, WHITE, True, PP_ALIGN.CENTER, first=True, sa=0)
        ll = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(cx), Inches(y + 0.5), Inches(cx), Inches(bottom))
        ll.line.color.rgb = C("hair"); ll.line.width = Pt(1.5); ll.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    for i, m in enumerate(msgs):
        yy = y + 0.85 + i * step; x1 = xs.get(m.get("from"), x); x2 = xs.get(m.get("to"), x + w)
        c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(yy), Inches(x2), Inches(yy))
        c.line.color.rgb = C("accent2" if m.get("emphasis") else "ink"); c.line.width = Pt(1.75); _arrow(c)
        lx = min(x1, x2); t = tb(slide, lx, yy - 0.32, abs(x2 - x1), 0.3, MSO_ANCHOR.BOTTOM)
        para(t, m.get("label", ""), 12, C("ink"), align=PP_ALIGN.CENTER, first=True, sa=0)
def ex_code(slide, text, x, y, w, h, caption):
    rrect(slide, x, y, w, h, C("dark"), None, rad=0.03)
    t = tb(slide, x+0.3, y+0.25, w-0.6, h-0.5)
    for ln in str(text).splitlines() or [""]:
        p = para(t, ln, 15, WHITE, font=FM, align=PP_ALIGN.LEFT, sa=2, first=(t.paragraphs[0].runs == []))
        p._p.get_or_add_pPr().set('rtl', '0')   # code is LTR even in RTL decks

def ex_devices(slide, ex, x, y, w, h):
    """Generic device frames (blueprint_lib.device_geometry): editable shapes + the screenshot inside."""
    D = bl.DEVICE_COLORS
    items = []
    for d in bl.exhibit_devices(ex):
        path = A.file_for(d["ref"], raster_only=True)
        items.append({**d, "path": path, "ar": bl.image_ar(path),
                      "alt": d.get("alt") or ex.get("alt") or A.alt(d["ref"], ex.get("caption", ""))})
    W, H, placed = bl.device_row(items, RTL, arrangement=ex.get("arrangement", "row"))
    cap = ex.get("caption", ""); ch = 0.34 if cap else 0
    LH = 0.13 if any(it.get("label") for it in items) else 0.0
    k = min(w / W, (h - ch) / (H + LH))
    ox = x + (w - W * k) / 2; oy = y + (h - ch - (H + LH) * k) / 2
    def shape(kind, X, Y, Ww, Hh, r, fill, line=None):
        if kind == "oval":
            sp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(X), Inches(Y), Inches(Ww), Inches(Hh))
            sp.fill.solid(); sp.fill.fore_color.rgb = RGB(fill); sp.line.fill.background(); sp.shadow.inherit = False
            return sp
        sp = rrect(slide, X, Y, Ww, Hh, RGB(fill), RGB(line) if line else None, rad=min(0.5, r / max(1e-6, min(Ww, Hh))) or 0.0001, shadow=False)
        return sp
    for it, g, px, py, sc in placed:
        f = lambda v: v * sc * k
        for pt in g["parts"]:
            X, Y = ox + (px + pt["x"] * sc) * k, oy + (py + pt["y"] * sc) * k
            Ww, Hh, r = f(pt["w"]), f(pt["h"]), f(pt["r"])
            kd = pt["kind"]
            if kd in ("camera", "dot"):
                shape("oval", X, Y, Ww, Hh, r, D[kd])
            elif kd == "screen":
                shape("rect", X, Y, Ww, Hh, r, D["web"] if g["device"] == "browser" else D["screen"])
                if it["path"]:
                    pic = fitted(slide, it["path"], X, Y, Ww, Hh, it["alt"])
                    if r > 0.001 and abs(pic.width - Inches(Ww)) < Inches(0.02) and abs(pic.height - Inches(Hh)) < Inches(0.02):
                        geom = pic._element.spPr.find(qn("a:prstGeom"))
                        if geom is not None:
                            geom.set("prst", "roundRect")
                            for c in list(geom): geom.remove(c)
                            geom.append(parse_xml('<a:avLst %s><a:gd name="adj" fmla="val %d"/></a:avLst>'
                                                  % (nsdecls("a"), int(100000 * min(0.5, r / min(Ww, Hh))))))
                else:
                    para(tb(slide, X, Y, Ww, Hh, MSO_ANCHOR.MIDDLE), "[%s]" % it["ref"], 11, C("mute"), align=PP_ALIGN.CENTER, first=True)
            elif kd == "body":
                shape("rect", X, Y, Ww, Hh, r, D["body"], D["edge"])
            elif kd == "pill":
                shape("rect", X, Y, Ww, Hh, r, D["pill"])
                if ex.get("url"):
                    t = tb(slide, X, Y, Ww, Hh, MSO_ANCHOR.MIDDLE)
                    pp = para(t, ex["url"], max(6, Hh * 72 * 0.45), C("mute"), align=PP_ALIGN.CENTER, first=True, sa=0)
                    pp._p.get_or_add_pPr().set("rtl", "0")
            elif kd == "chrome":
                shape("rect", X, Y, Ww, Hh, r, D["chrome"], D["dot"])
            else:
                shape("rect", X, Y, Ww, Hh, r, D.get(kd, D["body"]))
        lp = bl.loupe_geometry(g["screen"], it["ar"], it.get("loupe")) if it["path"] else None
        if lp:
            d = f(lp["d"]); LX = ox + (px + (lp["cx"] - lp["d"] / 2) * sc) * k; LY = oy + (py + (lp["cy"] - lp["d"] / 2) * sc) * k
            ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(LX - d * 0.03), Inches(LY - d * 0.03), Inches(d * 1.06), Inches(d * 1.06))
            ring.line.fill.background(); ring.shadow.inherit = False; alpha_fill(ring, "000000", 18)
            pic = slide.shapes.add_picture(it["path"], Inches(LX), Inches(LY), Inches(d), Inches(d))
            pic.crop_left, pic.crop_top, pic.crop_right, pic.crop_bottom = lp["crop"]
            geom = pic._element.spPr.find(qn("a:prstGeom"))
            if geom is not None: geom.set("prst", "ellipse")
            pic.line.color.rgb = WHITE; pic.line.width = Pt(2.25)
            set_alt(pic, (it["alt"] + " — " if it["alt"] else "") + "detail")
        if it.get("label"):
            cx = ox + (px + g["W"] * sc / 2) * k
            para(tb(slide, cx - 1.2, oy + H * k + 0.02, 2.4, LH * k, MSO_ANCHOR.TOP), it["label"], max(10, LH * k * 72 * 0.45),
                 C("mute"), True, PP_ALIGN.CENTER, first=True, sa=0)
    if cap:
        para(tb(slide, x, y + h - ch, w, ch, MSO_ANCHOR.MIDDLE), cap, 10.5, C("mute"), align=AL_MAIN, sa=0, first=True)

def place_exhibit(slide, ex, box, bleed=False):
    x, y, w, h = box; t = ex.get("type"); cap = ex.get("caption", "")
    if bl.exhibit_devices(ex): ex_devices(slide, ex, x, y, w, h); return
    if t in ("screenshot", "image"): ex_image(slide, ex.get("ref"), x, y, w, h, cap, ex.get("alt", ""), bleed)
    elif t == "chart": ex_chart(slide, ex.get("data", {}), x, y, w, h - (0.35 if cap else 0)); cap and para(tb(slide, x, y+h-0.32, w, 0.3), cap, 10.5, C("mute"), first=True, sa=0)
    elif t == "table": ex_table(slide, ex.get("data", {}), x, y, w, min(h, 0.5 * (len(ex.get("data", {}).get("rows", [])) + 1)))
    elif t == "diagram":
        dd = ex.get("data", {}); k = dd.get("kind", "chain")
        if k == "sequence": ex_sequence(slide, dd, x, y, w, h - 0.4)
        elif k == "timeline": ex_timeline(slide, dd, x, y, w, min(h, 2.2))
        else: ex_chain(slide, dd, x, y, w, min(h, 1.9))
        if cap: para(tb(slide, x, y + (h - 0.35 if k == "sequence" else min(h, 2.2 if k == "timeline" else 1.9) + 0.15), w, 0.35), cap, 13, C("mute"), italic=True, first=True, sa=0)
    elif t == "code": ex_code(slide, ex.get("data", ""), x, y, w, h, cap)

# ---------- text column + engagement ----------
LINKS = []   # (shape, target slide id) resolved after all slides exist
def bullets_box(slide, bullets, x, y, w, h, size=17):
    if not bullets: return 0
    tf = tb(slide, x, y, w, h); first = True
    for b in bullets:
        parts = [("▪  ", {"color": C("accent"), "bold": True, "size": size - 4})]
        if b.get("lead"): parts.append((b["lead"]+"  ", {"color": C("ink"), "bold": True, "size": size}))
        parts.append((b.get("text", ""), {"color": C("mute"), "size": size * BS, "font": FM if b.get("mono") else None}))
        runs_para(tf, parts, align=AL_MAIN, sa=12, line=1.18, first=first); first = False
    return min(h, 0.62 * len(bullets) + 0.2)
def engagement_box(slide, sl, x, y, w, h, dark=False):
    eng = sl.get("engagement") or {}; t = eng.get("type")
    if not t or t == "none" or sl.get("_answerFor"): return
    label = {"poll": S["question"], "activity": S["activity"], "demo": S["demo"]}.get(t, S["question"])
    opts = eng.get("options") or []
    tf = tb(slide, x, y, w, 0.9)
    para(tf, label, 11, C("accent"), True, first=True, sa=2)
    if eng.get("prompt"): para(tf, eng["prompt"], 17, WHITE if dark else C("ink"), True, sa=4, line=1.1)
    oy = y + 0.95
    if opts and t in ("quiz", "question", "poll"):
        oh = min(0.5, (h - 1.3) / max(len(opts), 1))
        for o in opts:
            sp = rrect(slide, x, oy, w, oh - 0.08, WHITE, C("hair"), rad=0.18, shadow=False, name="opt_" + o["id"])
            st = sp.text_frame; st.word_wrap = True
            for m in ("margin_left", "margin_right"): setattr(st, m, Inches(0.18))
            st.vertical_anchor = MSO_ANCHOR.MIDDLE
            para(st, o.get("text", ""), 14, C("ink"), first=True, sa=0)
            if eng.get("correctOptionId"):
                place = eng.get("answerPlacement") or ("inline" if meta.get("deliveryMode") == "self-read" else "next-slide")
                if place != "inline": LINKS.append((sp, sl["id"] + "__answer"))
            oy += oh
        if not eng.get("correctOptionId"):
            para(tb(slide, x, oy + 0.02, w, 0.3), S["poll"].split(":")[0], 10, C("mute"), first=True, sa=0)
        elif (eng.get("answerPlacement") == "inline") or (meta.get("deliveryMode") == "self-read" and not eng.get("answerPlacement")):
            ctext = next((o.get("text", "") for o in opts if o["id"] == eng["correctOptionId"]), "")
            para(tb(slide, x, oy + 0.02, w, 0.4), "%s: %s" % (S["answer"], ctext), 13, C("ink"), True, first=True, sa=0)
    elif t == "demo":
        if eng.get("assetRef"): ex_image(slide, eng["assetRef"], x, oy, w, max(1.0, h - 1.5), "", eng.get("prompt", ""))
        if eng.get("url"): para(tb(slide, x, y + h - 0.35, w, 0.3), eng["url"], 12, C("accent"), first=True, sa=0, url=eng["url"])

# ---------- slide renderers ----------
def statement_block(s, sl, title, bullets, dark=True, kicker=None):
    center = TOK["coverAlign"] == "center"
    al = PP_ALIGN.CENTER if center else AL_MAIN
    tf = tb(s, MG + 0.25, 1.6, CW - 0.5, 4.0, MSO_ANCHOR.MIDDLE)
    first = True
    if sl.get("role") == "divider" and sec_index(sl):
        para(tf, "%02d" % sec_index(sl), 90, C("accent2"), True, al, FD, sa=4, first=True); first = False
    k = kicker_text(sl, kicker) if kicker else ""
    if k: para(tf, k, 14, MUTE_D if dark else C("accent"), True, al, FB, sa=10, first=first); first = False
    para(tf, title or "", max(24, 36 * TS * bl.title_scale_for(title)), WHITE if dark else C("ink"), BOLDT, al, FD, sa=14, line=1.08, first=first)
    for b in bullets or []:
        para(tf, b.get("text", ""), 19, MUTE_D if dark else C("mute"), align=al, sa=6, line=1.15)
    engagement_box(s, sl, MG + 0.25, 5.3, min(CW - 0.5, 7.0), 1.6, dark)

def render(sl, n):
    role = sl.get("role", "concept"); lay = sl.get("layout")
    dark = sl.get("dark", role in ("cover", "stakes", "close", "quote", "divider"))
    bgk = (sl.get("background") or {})
    s = prs.slides.add_slide(BLANK); bg(s, dark, bgk.get("assetRef") or bgk.get("photo")); motif(s, sl, dark, n)
    title = sl.get("actionTitle", ""); kicker = sl.get("kicker", "")
    bullets = sl.get("bullets", []); ex = sl.get("exhibit"); eng = sl.get("engagement") or {}
    has_eng = eng.get("type") not in (None, "none") and not sl.get("_answerFor")
    top = 2.1 if TOK["motif"] != "rule" else 2.25

    if role == "cover" and not lay:
        center = TOK["coverAlign"] == "center"; al = PP_ALIGN.CENTER if center else AL_MAIN
        tf = tb(s, MG + 0.25, 2.0, CW - 0.5, 2.8, MSO_ANCHOR.MIDDLE if center else MSO_ANCHOR.TOP)
        if kicker: para(tf, kicker, 20, MUTE_D, True, al, FB, sa=10, first=True)
        para(tf, title or meta.get("title", ""), max(32, 54 * TS * bl.title_scale_for(title)), WHITE, BOLDT, al, FD, sa=6, line=1.0, first=(not kicker))
        if meta.get("subtitle"): para(tf, meta["subtitle"], 20, MUTE_D, align=al, sa=0)
        foot = tb(s, MG + 0.25, 6.2, CW - 0.5, 0.8)
        if meta.get("authors"): para(foot, "  ·  ".join(meta["authors"]), 16, C("accent"), True, al, FB, sa=2, first=True)
        line2 = "   ·   ".join([x for x in [meta.get("event"), meta.get("date")] if x])
        if line2: para(foot, line2, 12.5, MUTE_D, align=al, font=FM, sa=0, first=not meta.get("authors"))
    elif lay == "statement" or (not lay and role in ("stakes", "close", "quote", "divider")):
        statement_block(s, sl, title, bullets, dark=dark, kicker=kicker if lay else None)
        if sl.get("_answerFor"):
            b = rrect(s, MG + 0.25, 6.2, 2.8, 0.45, False, C("hair"), rad=0.2, shadow=False, name="back")
            para(b.text_frame, "← " + S["back"] if not RTL else S["back"] + " →", 12, C("accent"), True, PP_ALIGN.CENTER, first=True, sa=0)
            LINKS.append((b, sl["_answerFor"]))
    elif lay == "big-number":
        bn = (ex or {}).get("bigNumber") or {}
        k = kicker_text(sl, kicker)
        if k: para(tb(s, MG, 1.0, CW, 0.4), k, 13.5, C("accent"), True, first=True, sa=0)
        tf = tb(s, MG, 1.45, CW, 2.2, MSO_ANCHOR.BOTTOM, name="!!bignum")
        p = para(tf, bl.ltr(bn.get("value", ""), RTL), 120, C("accent2"), True, font=FD, first=True, sa=0, line=0.9)
        if bn.get("unit"): run(p, bl.ltr(" " + bn["unit"], RTL), 48, C("accent"), True, FD)
        if bn.get("context"): para(tb(s, MG, 3.7, CW, 0.4), bn["context"], 14, C("mute"), first=True, sa=0)
        para(tb(s, MG, 4.2, CW * 0.85, 1.2, name="!!title"), title, max(24, 32 * TS * bl.title_scale_for(title)), WHITE if dark else C("ink"), BOLDT, font=FD, first=True, sa=0, line=1.05)
        bullets_box(s, bullets, MG, 5.45, CW, 1.4, 16)
        if has_eng: engagement_box(s, sl, MG + CW * 0.55, 5.4, CW * 0.45, 1.5, dark)
    elif lay == "split":
        side = (ex or {}).get("side", "left")
        half = 13.333 / 2
        vx = 0 if side == "left" else half; txx = (half + 0.55) if side == "left" else MG
        tw = half - 0.55 - MG
        photo = ex and ex.get("type") == "image" and not bl.exhibit_devices(ex)
        if not photo:
            panel = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(vx), 0, Inches(half), SH)
            panel.fill.solid(); panel.fill.fore_color.rgb = C("bgAlt"); panel.line.fill.background(); panel.shadow.inherit = False
        if ex: place_exhibit(s, ex, (vx, 0, half, 7.5) if photo else (vx + 0.45, 1.0, half - 0.9, 5.5), bleed=bool(photo))
        header(s, sl, kicker, title, dark, size=27, x=txx, w=tw, y0=1.4)
        bh = bullets_box(s, bullets, txx, 3.3, tw, 2.4, 16)
        if has_eng: engagement_box(s, sl, txx, 3.3 + bh + 0.1, tw, 3.4 - bh, dark)
    elif lay == "full-exhibit":
        header(s, sl, kicker, title, dark, size=26)
        if ex: place_exhibit(s, ex, (MG, top - 0.15, CW, 4.55))
        if bullets: para(tb(s, MG, 6.45, CW, 0.4), " · ".join(b.get("text", "") for b in bullets), 14, C("mute"), first=True, sa=0)
    elif role == "agenda":
        header(s, sl, kicker, title, dark=dark)
        secs = SECTIONS; nn = max(1, len(secs)); gap = 0.4; cw = (CW-gap*(nn-1))/nn
        for i, sec in enumerate(secs):
            xi = MG + (nn-1-i)*(cw+gap) if RTL else MG + i*(cw+gap)
            rrect(s, xi, 2.6, cw, 3.2, C("dark") if dark else WHITE, None if dark else C("hair"))
            t = tb(s, xi+0.3, 3.0, cw-0.6, 2.4)
            para(t, "%02d" % (i+1), 40, C("accent2"), True, AL_MAIN, FD, sa=8, first=True)
            para(t, sec.get("title", ""), 24, WHITE if dark else C("ink"), True, AL_MAIN, FD, sa=0)
    elif role in ("references", "appendix"):
        header(s, sl, kicker if kicker != title else "", title or ("References" if role == "references" else "Appendix"), dark=dark)
        tf = tb(s, MG, top, CW, 4.8)
        if sl.get("_entries"):
            for e in sl["_entries"]:
                p = para(tf, bl.entry_text(e, RTL), 13.5, C("mute"), align=AL_MAIN, sa=8, first=(tf.paragraphs[0].runs == []))
                if e.get("url"):
                    run(p, (bl.RLM if RTL else "") + " — ", 13.5, C("mute"))
                    run(p, bl.ltr(bl.url_label(e["url"]), RTL), 13.5, C("accent"), url=e["url"])
        else:
            for b in bullets or []:
                para(tf, b.get("text", ""), 15, C("mute"), align=AL_MAIN, sa=8, first=(tf.paragraphs[0].runs == []))
    elif ex and (role == "process" or ex.get("type") == "diagram"):
        header(s, sl, kicker, title, dark=dark)
        dk = (ex.get("data") or {}).get("kind")
        hh = 3.6 if dk == "sequence" else 1.9
        place_exhibit(s, ex, (MG, top + 0.5, CW, hh))
        y = top + 0.5 + hh + (0.1 if dk == "sequence" else 0.65)
        bh = bullets_box(s, bullets, MG, y, CW, 6.85 - y, 16)
        if has_eng: engagement_box(s, sl, MG, y + bh, CW * 0.6, 6.85 - y - bh, dark)
    elif ex and (role == "comparison" or ex.get("type") == "table"):
        header(s, sl, kicker, title, dark=dark)
        rows = len((ex.get("data") or {}).get("rows", [])) + 1
        th = min(3.6, 0.5 * rows)
        place_exhibit(s, ex, (MG + 0.25, top + 0.3, CW - 0.5, th))
        bh = bullets_box(s, bullets, MG + 0.25, top + 0.55 + th, CW - 0.5, 6.85 - (top + 0.55 + th), 15)
        if has_eng: engagement_box(s, sl, MG + 0.25, top + 0.6 + th + bh, CW * 0.6, 6.85 - (top + 0.6 + th + bh), dark)
    else:  # concept / evidence with or without an exhibit
        header(s, sl, kicker, title, dark=dark)
        cdw = CW * 0.47; txw = CW * 0.47; gap = CW - cdw - txw
        side = (ex or {}).get("side", "left")
        cx = MG if side == "left" else MG + txw + gap
        tx = MG + cdw + gap if side == "left" else MG
        if ex: place_exhibit(s, ex, (cx, top - 0.05, cdw, 4.65))
        w = txw if ex else CW
        x = tx if ex else MG
        bh = bullets_box(s, bullets, x, top + 0.2, w, 4.2, 17)
        if has_eng: engagement_box(s, sl, x, top + 0.2 + bh, min(w, 7.0), 4.5 - bh, dark)

    footer(s, sl, dark)
    notes = sl.get("speakerNotes", "")
    if eng.get("presenterCue") and not sl.get("_answerFor"): notes = (notes + "\n\n" if notes else "") + "▶ " + eng["presenterCue"]
    if notes: s.notes_slide.notes_text_frame.text = notes
    return s

for n, sl in enumerate(SLIDES, 1):
    render(sl, n)

# ---------- internal links (quiz option -> answer slide, answer -> back) ----------
by_id = {sl["id"]: prs.slides[i] for i, sl in enumerate(SLIDES)}
for shape, target in LINKS:
    if target in by_id: shape.click_action.target_slide = by_id[target]

# ---------- names, Morph, Sections ----------
ZOOM = (BP.get("navigation", {}).get("mode") == "zoom")
MORPH = ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
         'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
         '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
         '<p:transition spd="slow" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" p14:dur="1400">'
         '<p159:morph option="byObject"/></p:transition></mc:Choice>'
         '<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')
FADE = '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med"><p:fade/></p:transition>'
for si, (sl, data) in enumerate(zip(prs.slides, SLIDES), 1):
    for k, sh in enumerate(sl.shapes):
        if not sh.name.startswith("!!"): sh.name = "s%d_%d" % (si, k)
    tr = (data.get("animation") or {}).get("transition")
    xml = MORPH if (tr == "morph" or (ZOOM and si > 1)) else (FADE if tr in ("fade", "push") else None)
    if xml:
        el = parse_xml(xml); clr = sl._element.find(qn('p:clrMapOvr'))
        (clr.addnext(el) if clr is not None else sl._element.cSld.addnext(el))

if ZOOM and SECTIONS:
    idx = {s["id"]: i for i, s in enumerate(SLIDES)}
    sldIds = [c.get('id') for c in prs.slides._sldIdLst]
    secs = ""
    for sec in SECTIONS:
        ids = "".join('<p14:sldId id="%s"/>' % sldIds[idx[sid]] for sid in sec.get("slideIds", []) if sid in idx)
        if not ids: continue
        secs += '<p14:section name="%s" id="{%s}"><p14:sldIdLst>%s</p14:sldIdLst></p14:section>' % (
            sec["title"].replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;"), str(uuid.uuid4()).upper(), ids)
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
for w in A.warnings: print("warning:", w)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst), "| rtl:", RTL, "| zoom:", ZOOM, "| system:", d.get("system") or SYS)
