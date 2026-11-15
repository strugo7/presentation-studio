# -*- coding: utf-8 -*-
# Interpret our own generated PPTX (pictures, rounded boxes, text boxes, one table) as HTML for Chrome -> PDF.
import sys, os, io, base64, html
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from PIL import Image

SRC, OUTDIR = sys.argv[1], sys.argv[2]
FONT = os.path.expanduser("~/Library/Fonts/Assistant-VariableFont_wght.ttf")
os.makedirs(os.path.join(OUTDIR, "img"), exist_ok=True)

def px(v):
    return Emu(v).inches * 96.0

def css_color(c):
    try:
        return "#%02X%02X%02X" % (c[0], c[1], c[2])
    except Exception:
        return "#000"

def fill_of(sh):
    try:
        if sh.fill.type == 1:
            return css_color(sh.fill.fore_color.rgb)
    except Exception:
        pass
    return None

def line_of(sh):
    try:
        if sh.line.fill.type == 1:
            return css_color(sh.line.color.rgb), max(1.0, sh.line.width.pt * 96 / 72)
    except Exception:
        pass
    return None

def has_shadow(sh):
    try:
        eff = sh._element.spPr.find(qn("a:effectLst"))
        return eff is not None and eff.find(qn("a:outerShdw")) is not None
    except Exception:
        return False

ALIGN = {PP_ALIGN.RIGHT: "right", PP_ALIGN.LEFT: "left", PP_ALIGN.CENTER: "center"}

def para_html(p):
    runs = []
    for r in p.runs:
        f = r.font
        size = f.size.pt if f.size else 16
        fam = "Courier New, Menlo, monospace" if (f.name and "Courier" in f.name) else "Assistant"
        try:
            col = css_color(f.color.rgb)
        except Exception:
            col = "#000"
        st = "font-size:%.2fpt;font-weight:%d;font-style:%s;color:%s;font-family:%s" % (
            size, 700 if f.bold else 400, "italic" if f.italic else "normal", col, fam)
        runs.append('<span style="%s">%s</span>' % (st, html.escape(r.text)))
    if not runs:
        return ""
    pPr = p._p.find(qn("a:pPr"))
    rtl = pPr is not None and pPr.get("rtl") == "1"
    al = ALIGN.get(p.alignment, "right" if rtl else "left")
    sb = p.space_before.pt if p.space_before is not None else 0
    sa = p.space_after.pt if p.space_after is not None else 0
    lh = ""
    if p.line_spacing is not None and isinstance(p.line_spacing, float):
        lh = "line-height:%.3f;" % (1.28 * p.line_spacing)
    return '<p dir="%s" style="text-align:%s;margin:%.2fpt 0 %.2fpt 0;%s">%s</p>' % (
        "rtl" if rtl else "ltr", al, sb, sa, lh or "line-height:1.28;", "".join(runs))

def frame_html(tf, x, y, w, h, extra=""):
    anchor = {MSO_ANCHOR.MIDDLE: "center", MSO_ANCHOR.BOTTOM: "flex-end"}.get(tf.vertical_anchor, "flex-start")
    pad = "%.1fpx %.1fpx %.1fpx %.1fpx" % (px(tf.margin_top or 0), px(tf.margin_right or 0),
                                          px(tf.margin_bottom or 0), px(tf.margin_left or 0))
    body = "".join(para_html(p) for p in tf.paragraphs)
    return ('<div style="position:absolute;left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;display:flex;'
            'flex-direction:column;justify-content:%s;padding:%s;box-sizing:border-box;white-space:pre-wrap;%s">%s</div>'
            % (x, y, w, h, anchor, pad, extra, body))

def table_html(sh):
    t = sh.table
    x, y = px(sh.left), px(sh.top)
    cols = "".join('<col style="width:%.1fpx">' % px(c.width) for c in t.columns)
    rows = []
    for ri, r in enumerate(t.rows):
        cells = []
        for ci in range(len(t.columns)):
            c = t.cell(ri, ci)
            bg = ""
            try:
                if c.fill.type == 1:
                    bg = "background:%s;" % css_color(c.fill.fore_color.rgb)
            except Exception:
                pass
            pad = "%.1fpx %.1fpx %.1fpx %.1fpx" % (px(c.margin_top), px(c.margin_right), px(c.margin_bottom), px(c.margin_left))
            inner = "".join(para_html(p) for p in c.text_frame.paragraphs)
            cells.append('<td style="%spadding:%s;vertical-align:middle;border:1px solid #fff">%s</td>' % (bg, pad, inner))
        rows.append('<tr style="height:%.1fpx">%s</tr>' % (px(r.height), "".join(cells)))
    return ('<table dir="rtl" style="position:absolute;left:%.1fpx;top:%.1fpx;width:%.1fpx;table-layout:fixed;'
            'border-collapse:collapse"><colgroup>%s</colgroup>%s</table>' % (x, y, px(sh.width), cols, "".join(rows)))

prs = Presentation(SRC)
W, H = px(prs.slide_width), px(prs.slide_height)
n_img = 0
slides_html = []
for si, slide in enumerate(prs.slides, 1):
    parts = []
    for sh in slide.shapes:
        x, y, w, h = px(sh.left), px(sh.top), px(sh.width), px(sh.height)
        if sh.shape_type == 13:  # picture
            n_img += 1
            im = Image.open(io.BytesIO(sh.image.blob)).convert("RGB")
            fn = "img/i%03d.jpg" % n_img
            im.save(os.path.join(OUTDIR, fn), "JPEG", quality=88, optimize=True)
            parts.append('<img src="%s" style="position:absolute;left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx">' % (fn, x, y, w, h))
        elif sh.has_table if hasattr(sh, "has_table") else False:
            parts.append(table_html(sh))
        else:
            fill, line = fill_of(sh), line_of(sh)
            if fill or line:
                rad = 0
                try:
                    rad = sh.adjustments[0] * min(w, h)
                except Exception:
                    pass
                st = "position:absolute;left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;border-radius:%.1fpx;box-sizing:border-box;" % (x, y, w, h, rad)
                if fill: st += "background:%s;" % fill
                if line: st += "border:%.1fpx solid %s;" % (line[1], line[0])
                if has_shadow(sh): st += "box-shadow:0 3px 10px rgba(26,34,48,.2);"
                parts.append('<div style="%s"></div>' % st)
            if sh.has_text_frame and sh.text_frame.text.strip():
                parts.append(frame_html(sh.text_frame, x, y, w, h))
    slides_html.append('<section class="s">%s</section>' % "".join(parts))

b64 = base64.b64encode(open(FONT, "rb").read()).decode()
doc = """<!DOCTYPE html><html lang="he"><head><meta charset="utf-8"><style>
@font-face{font-family:"Assistant";src:url(data:font/ttf;base64,%s) format("truetype");font-weight:200 800}
@page{size:%.0fpx %.0fpx;margin:0}
html,body{margin:0;padding:0;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.s{position:relative;width:%.0fpx;height:%.0fpx;overflow:hidden;break-after:page;page-break-after:always;font-family:Assistant,sans-serif}
</style></head><body>%s</body></html>""" % (b64, W, H, W, H, "".join(slides_html))
with open(os.path.join(OUTDIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(doc)
print("slides:", len(slides_html), "| images:", n_img, "| page px:", round(W), "x", round(H))
