# -*- coding: utf-8 -*-
"""Shared logic for every renderer: loading + normalising a blueprint, validation (schema +
cross-references), asset resolution with stable unique names, sources/citations/credits, synthetic
slides (quiz answers, sources pages), design-system tokens, chart normalisation and stage merging.

Pure stdlib. `jsonschema` is used for schema validation when it is installed; the cross-reference
checks run either way. Both render_html.py and render_pptx.py import this so the formats stay in step.
"""
import copy
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "blueprint.schema.json")
FONT_DIR = os.path.join(HERE, "fonts")
DEFAULT_FONT = os.path.join(FONT_DIR, "Assistant[wght].ttf")
DEFAULT_FONT_FAMILY = "Assistant"

DEFAULT_PALETTE = {"bg": "FFFFFF", "bgAlt": "F6F7F9", "ink": "1A2230", "mute": "5B6472",
                   "accent": "2C5F7C", "accent2": "B4722E", "hair": "E2E5EA", "dark": "1C2A3A"}

LAYOUTS = ("statement", "split", "full-exhibit", "big-number")
CHART_KINDS = ("column", "bar", "line", "scatter")
DIAGRAM_KINDS = ("chain", "timeline", "sequence")
RTL_LANGS = ("he", "ar", "fa", "ur", "yi")
RASTER_EXT = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff")

# ---------------------------------------------------------------------------------------------
# Design-system tokens. These are what make `design.system` change composition, not just colour.
#   titleScale   multiplier on the base title size      titleWeight  400..800
#   coverAlign   start | center                         motif        grid | none | rule | numbers
#   frame        card | hairline | bleed                margin       px at 1920 wide (144 px = 1 in)
#   kicker       accent | caps | number                 lightBg      bg | bgAlt  (content canvas)
#   bodyScale    multiplier on body size                radius       exhibit corner radius px
# Every preset id that already existed is kept. Aliases add new directions on top of a preset.
# ---------------------------------------------------------------------------------------------
SYSTEM_TOKENS = {
    "cobalt-grid": {"titleScale": 1.0, "titleWeight": 800, "coverAlign": "start", "motif": "grid",
                    "frame": "card", "margin": 110, "kicker": "accent", "lightBg": "bg",
                    "bodyScale": 1.0, "radius": 18},
    "signal": {"titleScale": 0.95, "titleWeight": 800, "coverAlign": "start", "motif": "rule",
               "frame": "card", "margin": 110, "kicker": "caps", "lightBg": "bg",
               "bodyScale": 1.0, "radius": 10},
    "swiss": {"titleScale": 1.1, "titleWeight": 700, "coverAlign": "start", "motif": "numbers",
              "frame": "hairline", "margin": 130, "kicker": "number", "lightBg": "bg",
              "bodyScale": 1.0, "radius": 0,
              "palette": {"accent": "D52B1E", "accent2": "D52B1E", "ink": "111111", "mute": "4A4A4A",
                          "dark": "111111", "hair": "DADADA", "bgAlt": "F4F4F4"}},
    "editorial": {"titleScale": 1.3, "titleWeight": 400, "coverAlign": "center", "motif": "none",
                  "frame": "bleed", "margin": 150, "kicker": "caps", "lightBg": "bgAlt",
                  "bodyScale": 1.05, "radius": 0,
                  "palette": {"bgAlt": "FBFAF7", "accent": "8C3B2E", "accent2": "C08A2D",
                              "ink": "1E1B18", "mute": "5E5850", "dark": "1E1B18", "hair": "E6E1D8"}},
    "mono": {"titleScale": 1.0, "titleWeight": 700, "coverAlign": "start", "motif": "rule",
             "frame": "hairline", "margin": 130, "kicker": "caps", "lightBg": "bg",
             "bodyScale": 1.0, "radius": 0,
             "palette": {"accent": "1A1A1A", "accent2": "1A1A1A", "ink": "1A1A1A", "mute": "555555",
                         "dark": "1A1A1A", "hair": "D9D9D9", "bgAlt": "F5F5F2"}},
}
SYSTEM_TOKENS["custom"] = dict(SYSTEM_TOKENS["cobalt-grid"])

# alias -> (base preset, token overrides). Documented in deck-designer/references/design-systems.md.
SYSTEM_ALIASES = {
    "editorial-report": ("editorial", {"titleScale": 1.15, "coverAlign": "start", "motif": "rule"}),
    "product-demo": ("cobalt-grid", {"motif": "none", "frame": "card", "radius": 22, "lightBg": "bgAlt"}),
    "executive-data-briefing": ("signal", {"titleScale": 0.9, "margin": 100, "kicker": "caps",
                                           "motif": "rule", "frame": "hairline", "radius": 0}),
    "classroom-workshop": ("cobalt-grid", {"titleScale": 1.05, "kicker": "number", "radius": 26,
                                           "bodyScale": 1.08,
                                           "palette": {"accent": "1F6F5C", "accent2": "D9822B",
                                                       "dark": "17322B", "bgAlt": "F3F7F5"}}),
    "keynote": ("editorial", {"titleScale": 1.45, "coverAlign": "center", "motif": "none",
                              "lightBg": "bg"}),
    "technical-case": ("swiss", {"kicker": "number", "motif": "numbers", "titleScale": 1.0,
                                 "palette": {"accent": "2C5F7C", "accent2": "C2410C", "dark": "16202B"}}),
}


def resolve_system(design):
    """Return (base_preset_id, tokens) for a blueprint's design block."""
    design = design or {}
    name = design.get("system") or "cobalt-grid"
    over = {}
    if name in SYSTEM_ALIASES:
        base, over = SYSTEM_ALIASES[name]
    else:
        base = name if name in SYSTEM_TOKENS else "cobalt-grid"
    tok = copy.deepcopy(SYSTEM_TOKENS[base])
    pal = dict(tok.pop("palette", {}))
    o = copy.deepcopy(over)
    pal.update(o.pop("palette", {}))
    tok.update(o)
    tok.update({k: v for k, v in (design.get("tokens") or {}).items()})  # explicit per-deck overrides
    tok["palette"] = pal
    if design.get("gridBackground") is False and tok["motif"] == "grid":
        tok["motif"] = "none"
    return base, tok


def palette(design):
    _, tok = resolve_system(design)
    return {**DEFAULT_PALETTE, **tok["palette"], **((design or {}).get("palette") or {})}


def _mix(a, b, t):
    """Blend hex colour a toward b by t (0..1)."""
    a, b = a.lstrip("#"), b.lstrip("#")
    return "".join("%02X" % round(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t) for i in (0, 2, 4))


def chart_colors(pal):
    """(series colours, highlight colour, single-series base colour) for both renderers.

    Series colours are always distinct, even in systems where accent == accent2 (swiss, mono), and
    a single-series highlight always differs from the other bars."""
    ser = []
    for k in ("accent", "accent2", "mute", "ink", "dark"):
        v = str(pal[k]).upper().lstrip("#")
        if v not in ser:
            ser.append(v)
    for t in (0.45, 0.7):  # lighter tints of the accent when the palette has too few distinct inks
        if len(ser) >= 4:
            break
        ser.append(_mix(ser[0], "FFFFFF", t))
    hl = str(pal["accent2"]).upper().lstrip("#")
    base = ser[1] if ser[0] == hl else ser[0]
    return ser[:4], hl, base


# ---------------------------------------------------------------------------------------------
# Localised UI strings the renderers print (sources pages, quiz controls, credits).
# ---------------------------------------------------------------------------------------------
STRINGS = {
    "en": {"sources": "Sources & credits", "source": "Source", "sourcesShort": "Sources",
           "credit": "Image", "accessed": "accessed", "answer": "Answer", "correct": "Correct.",
           "incorrect": "Not quite.", "reveal": "Reveal answer", "poll": "Local poll: counts on this device only",
           "back": "Back to the question", "usedOn": "slide", "license": "License", "try": "Choose an answer",
           "demo": "Demo", "activity": "Activity", "question": "Question", "cont": "cont."},
    "he": {"sources": "מקורות וקרדיטים", "source": "מקור", "sourcesShort": "מקורות",
           "credit": "תמונה", "accessed": "נבדק", "answer": "תשובה", "correct": "נכון.",
           "incorrect": "לא בדיוק.", "reveal": "חשיפת התשובה", "poll": "סקר מקומי: נספר במכשיר הזה בלבד",
           "back": "חזרה לשאלה", "usedOn": "שקף", "license": "רישיון", "try": "בחרו תשובה",
           "demo": "הדגמה", "activity": "פעילות", "question": "שאלה", "cont": "המשך"},
}


def strings(lang):
    return {**STRINGS["en"], **STRINGS.get((lang or "en").split("-")[0], {})}


# ---------------------------------------------------------------------------------------------
# Load + normalise (backward compatible: old blueprints and briefs keep working)
# ---------------------------------------------------------------------------------------------
def load(path):
    with open(path, encoding="utf-8") as f:
        return normalise(json.load(f))


def normalise(bp):
    bp = copy.deepcopy(bp)
    meta = bp.setdefault("meta", {})
    meta.setdefault("language", "en")
    if "rtl" not in meta:
        meta["rtl"] = meta["language"].split("-")[0] in RTL_LANGS
    aud = meta.get("audience")
    if isinstance(aud, dict) and "profile" not in aud and aud.get("who"):
        aud["profile"] = aud["who"]
    bp.setdefault("slides", [])
    bp.setdefault("assets", [])
    bp.setdefault("sources", [])
    return bp


def is_safe_url(u):
    return isinstance(u, str) and re.match(r"^https?://[^\s<>\"']+$", u) is not None


# ---------------------------------------------------------------------------------------------
# Validation: schema + cross-references
# ---------------------------------------------------------------------------------------------
def validate(bp, assets_dir=None):
    """Return (errors, warnings). Errors make the blueprint inconsistent; warnings are quality hints."""
    errors, warnings = [], []
    try:
        import jsonschema  # optional
        with open(SCHEMA_PATH, encoding="utf-8") as f:
            schema = json.load(f)
        v = jsonschema.Draft7Validator(schema)
        for e in sorted(v.iter_errors(bp), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in e.path) or "(root)"
            errors.append("schema: %s: %s" % (loc, e.message))
    except ImportError:
        warnings.append("jsonschema not installed: schema check skipped (cross-reference checks still ran)")

    slides = bp.get("slides", [])
    slide_ids = [s.get("id") for s in slides]
    dup = {i for i in slide_ids if slide_ids.count(i) > 1}
    for i in sorted(x for x in dup if x):
        errors.append("slides: duplicate slide id '%s'" % i)
    sid = set(slide_ids)

    src_ids = [s.get("id") for s in bp.get("sources", [])]
    for i in sorted({x for x in src_ids if src_ids.count(x) > 1}):
        errors.append("sources: duplicate source id '%s'" % i)
    srcs = set(src_ids)

    asset_ids = [a.get("id") for a in bp.get("assets", [])]
    for i in sorted({x for x in asset_ids if asset_ids.count(x) > 1}):
        errors.append("assets: duplicate asset id '%s'" % i)
    aset = set(asset_ids)

    sec_ids = {s.get("id") for s in bp.get("sections", [])}
    for sec in bp.get("sections", []):
        for x in sec.get("slideIds", []):
            if x not in sid:
                errors.append("sections[%s]: slideIds references unknown slide '%s'" % (sec.get("id"), x))

    def asset_ref_ok(ref, where):
        if not ref:
            return
        if ref in aset:
            return
        if assets_dir and os.path.exists(ref if os.path.isabs(ref) else os.path.join(assets_dir, ref)):
            return  # legacy: a bare path is still allowed
        if "/" in ref or "." in ref:
            warnings.append("%s: '%s' is a path, not an assets[] id; credit/licence can't be tracked" % (where, ref))
        else:
            errors.append("%s: references unknown asset '%s'" % (where, ref))

    for s in slides:
        w = "slide '%s'" % s.get("id")
        if s.get("section") and sec_ids and s["section"] not in sec_ids:
            errors.append("%s: section '%s' is not in sections[]" % (w, s["section"]))
        for c in s.get("citations", []) or []:
            if c.get("sourceId") not in srcs:
                errors.append("%s: citation sourceId '%s' does not resolve to sources[]" % (w, c.get("sourceId")))
        ex = s.get("exhibit") or {}
        if ex.get("type") in ("image", "screenshot"):
            asset_ref_ok(ex.get("ref"), w + " exhibit.ref")
        bg = s.get("background") or {}
        asset_ref_ok(bg.get("assetRef"), w + " background.assetRef")
        if ex.get("type") == "chart":
            d = ex.get("data") or {}
            k = d.get("kind", "column")
            if k in ("column", "bar", "line"):
                n = len(d.get("categories", []))
                for se in d.get("series", []):
                    if len(se.get("values", [])) != n:
                        errors.append("%s: chart series '%s' has %d values for %d categories"
                                      % (w, se.get("name", ""), len(se.get("values", [])), n))
                if k in ("column", "bar") and d.get("yMin") not in (None, 0):
                    warnings.append("%s: bar/column chart with a non-zero baseline exaggerates differences" % w)
            if not d.get("unit") and k != "scatter" and not ex.get("bigNumber"):
                warnings.append("%s: chart has no unit" % w)
        if s.get("layout") == "big-number" and not (ex.get("bigNumber") or {}).get("value"):
            warnings.append("%s: layout big-number without exhibit.bigNumber.value" % w)
        eng = s.get("engagement") or {}
        opts = [o.get("id") for o in eng.get("options", []) or []]
        if len(opts) != len(set(opts)):
            errors.append("%s: engagement option ids are not unique" % w)
        if eng.get("correctOptionId") and eng["correctOptionId"] not in opts:
            errors.append("%s: correctOptionId '%s' is not one of the options" % (w, eng["correctOptionId"]))
        if eng.get("assetRef"):
            asset_ref_ok(eng["assetRef"], w + " engagement.assetRef")
        if len(s.get("bullets", []) or []) > 3:
            warnings.append("%s: more than 3 bullets" % w)
        words = sum(len((b.get("text", "") + " " + b.get("lead", "")).split()) for b in s.get("bullets", []) or [])
        if words > 45:
            warnings.append("%s: ~%d words of body text (target <= 40)" % (w, words))

    nav = bp.get("navigation") or {}
    if nav.get("hubSlideId") and nav["hubSlideId"] not in sid:
        errors.append("navigation.hubSlideId '%s' is not a slide" % nav["hubSlideId"])
    for z in nav.get("zoomTargets", []) or []:
        if z not in sid:
            errors.append("navigation.zoomTargets: '%s' is not a slide" % z)

    for a in bp.get("assets", []):
        if a.get("kind") in ("photo", "image", "icon", "illustration") and not (a.get("credit") or a.get("license") or a.get("creator")):
            warnings.append("asset '%s': no credit/license recorded" % a.get("id"))
        if a.get("sourceUrl") and not is_safe_url(a["sourceUrl"]):
            errors.append("asset '%s': sourceUrl is not an http(s) URL" % a.get("id"))
    for s in bp.get("sources", []):
        if s.get("url") and not is_safe_url(s["url"]):
            errors.append("source '%s': url is not an http(s) URL" % s.get("id"))
    return errors, warnings


# ---------------------------------------------------------------------------------------------
# Assets: one resolver, stable collision-free output names, SVG/raster fallbacks
# ---------------------------------------------------------------------------------------------
def _slug(s):
    s = re.sub(r"[^A-Za-z0-9_-]+", "-", s or "").strip("-")
    return s[:40] or "asset"


class Assets:
    def __init__(self, bp, assets_dir):
        self.bp = bp
        self.dir = assets_dir
        self.by_id = {a["id"]: a for a in bp.get("assets", []) if a.get("id")}
        self.warnings = []

    def _abs(self, p):
        if not p:
            return None
        q = p if os.path.isabs(p) else os.path.join(self.dir, p)
        return q if os.path.exists(q) else None

    def record(self, ref):
        return self.by_id.get(ref)

    def candidates(self, ref):
        """Existing files for a ref (asset id or legacy path), primary first then fallbackPath."""
        a = self.by_id.get(ref)
        out = []
        if a:
            for k in ("path", "fallbackPath"):
                p = self._abs(a.get(k))
                if p:
                    out.append(p)
        else:
            p = self._abs(ref)
            if p:
                out.append(p)
        return out

    def file_for(self, ref, raster_only=False):
        """Best existing file for ref. raster_only=True skips SVG (python-pptx can't place SVG)."""
        if not ref:
            return None
        cands = self.candidates(ref)
        if raster_only:
            ras = [c for c in cands if os.path.splitext(c)[1].lower() in RASTER_EXT]
            if cands and not ras:
                self.warnings.append("asset '%s': only SVG available and no raster fallbackPath; placeholder used" % ref)
            return ras[0] if ras else None
        if not cands:
            self.warnings.append("asset '%s': file not found" % ref)
        return cands[0] if cands else None

    @staticmethod
    def dest_name(ref, src):
        """Stable, collision-free output file name: <slug>-<content hash8><ext>."""
        h = hashlib.sha1(open(src, "rb").read()).hexdigest()[:8]
        stem = _slug(ref if ref and "/" not in ref and "." not in ref else os.path.splitext(os.path.basename(src))[0])
        return "%s-%s%s" % (stem, h, os.path.splitext(src)[1].lower())

    def alt(self, ref, fallback=""):
        a = self.by_id.get(ref) or {}
        return a.get("alt") or fallback


# ---------------------------------------------------------------------------------------------
# Sources, citations, credits
# ---------------------------------------------------------------------------------------------
def source_numbers(bp):
    """Deck-wide citation numbers by order of first citation (uncited sources numbered after)."""
    order = []
    for s in bp.get("slides", []):
        for c in s.get("citations", []) or []:
            if c.get("sourceId") and c["sourceId"] not in order:
                order.append(c["sourceId"])
    for s in bp.get("sources", []):
        if s.get("id") not in order:
            order.append(s.get("id"))
    return {sid: i + 1 for i, sid in enumerate(order)}


def _src_short(src):
    return src.get("shortTitle") or src.get("title") or src.get("id")


def slide_footer(bp, slide, assets_ids=()):
    """One short line for the slide foot: numbered citations + image credits on this slide."""
    S = strings(bp.get("meta", {}).get("language"))
    nums = source_numbers(bp)
    by = {s.get("id"): s for s in bp.get("sources", [])}
    parts = []
    seen = set()
    for c in slide.get("citations", []) or []:
        sid = c.get("sourceId")
        if sid not in by:
            continue
        key = (sid, c.get("locator"))
        if key in seen:
            continue
        seen.add(key)
        t = "[%d]%s %s" % (nums[sid], RLM if bp.get("meta", {}).get("rtl") else "", _src_short(by[sid]))
        if c.get("locator"):
            t += ", " + c["locator"]
        parts.append(t)
    cred = []
    for aid in assets_ids:
        a = next((x for x in bp.get("assets", []) if x.get("id") == aid), None)
        if a and (a.get("credit") or a.get("creator")):
            c = a.get("credit") or " / ".join(x for x in (a.get("creator"), a.get("provider")) if x)
            if c not in cred:
                cred.append(c)
    out = ""
    if parts:
        out = S["sourcesShort"] + ": " + " · ".join(parts)
    if cred:
        out += ("   " if out else "") + S["credit"] + ": " + " · ".join(cred)
    return out


def slide_asset_ids(slide):
    ids = []
    ex = slide.get("exhibit") or {}
    if ex.get("ref"):
        ids.append(ex["ref"])
    for r in (ex.get("assetRefs") or []):
        ids.append(r)
    bg = slide.get("background") or {}
    if bg.get("assetRef"):
        ids.append(bg["assetRef"])
    eng = slide.get("engagement") or {}
    if eng.get("assetRef"):
        ids.append(eng["assetRef"])
    return ids


def source_entries(bp):
    """Entries for sources pages: [{n, parts, url}] (n=None for image credits).
    Credits are deduped by (credit, sourceUrl, license) and keep the slide numbers that use them.
    Renderers join `parts` with an isolating separator (bidi-safe in RTL); see entry_text()."""
    meta = bp.get("meta", {})
    S = strings(meta.get("language"))
    nums = source_numbers(bp)
    entries = []
    for s in sorted(bp.get("sources", []), key=lambda s: nums.get(s.get("id"), 999)):
        parts = []
        if s.get("creator"):
            parts.append(s["creator"])
        t = s.get("title") or s.get("id")
        if s.get("publishedAt"):
            t += " (%s)" % s["publishedAt"]
        parts.append(t)
        f = s.get("file")
        loc = s.get("url") or ((f.get("name") or f.get("path")) if isinstance(f, dict) else f)
        if loc and not is_safe_url(loc):
            parts.append(str(loc))
        if s.get("accessedAt"):
            parts.append("%s %s" % (S["accessed"], s["accessedAt"]))
        if s.get("license"):
            parts.append("%s: %s" % (S["license"], s["license"]))
        entries.append({"n": nums.get(s.get("id")), "parts": parts,
                        "url": s.get("url") if is_safe_url(s.get("url")) else None})
    used = {}
    for i, sl in enumerate(bp.get("slides", []), 1):
        for aid in slide_asset_ids(sl):
            used.setdefault(aid, []).append(i)
    groups = {}
    for a in bp.get("assets", []):
        if not (a.get("credit") or a.get("creator") or a.get("license")):
            continue
        key = (a.get("credit") or a.get("creator"), a.get("sourceUrl"), a.get("license"))
        g = groups.setdefault(key, {"a": a, "slides": []})
        g["slides"].extend(used.get(a.get("id"), []))
    for (credit, url, lic), g in groups.items():
        a = g["a"]
        parts = [S["credit"] + ": " + (credit or "")]
        if a.get("provider") and a.get("provider") not in (credit or ""):
            parts.append(a["provider"])
        if lic:
            parts.append("%s: %s" % (S["license"], lic))
        if g["slides"]:
            parts.append("%s %s" % (S["usedOn"], ", ".join(str(x) for x in sorted(set(g["slides"])))))
        entries.append({"n": None, "parts": parts, "url": url if is_safe_url(url) else None})
    return entries


RLM = "\u200f"


LRM = "\u200e"


def url_label(u):
    """Readable link text: the URL without scheme or trailing slash."""
    return re.sub(r"^https?://(www\.)?", "", u or "").rstrip("/")


def entry_text(e, rtl=False):
    """Plain-text form of a source entry (without its link). In RTL the separators and the [n] carry
    RLM marks so the number stays at the reading start and English titles don't reorder the line."""
    sep = (RLM + " — " + RLM) if rtl else " — "
    num = ("[%d]" % e["n"] + (RLM if rtl else "") + " ") if e.get("n") else ""
    return num + sep.join(e["parts"])


def ltr(text, rtl):
    """Keep a Latin/number token (e.g. '179.9 ms', '-46.5%') in visual LTR order inside RTL text."""
    return (LRM + str(text) + LRM) if rtl else str(text)


# ---------------------------------------------------------------------------------------------
# Synthetic slides: quiz answers + sources pages, per target
# ---------------------------------------------------------------------------------------------
def _answer_slide(bp, sl):
    S = strings(bp.get("meta", {}).get("language"))
    eng = sl.get("engagement") or {}
    opts = {o.get("id"): o.get("text", "") for o in eng.get("options", []) or []}
    corr = opts.get(eng.get("correctOptionId"), "")
    fb = eng.get("feedback") or {}
    expl = fb.get(eng.get("correctOptionId")) or fb.get("correct") or fb.get("explanation") or ""
    return {"id": sl["id"] + "__answer", "section": sl.get("section"), "role": "concept", "layout": "statement",
            "dark": False, "kicker": S["answer"] + (" · " + sl.get("kicker") if sl.get("kicker") else ""),
            "actionTitle": corr, "bullets": [{"text": expl}] if expl else [],
            "citations": sl.get("citations", []), "_answerFor": sl["id"],
            "speakerNotes": eng.get("presenterCue", "")}


def expand_slides(bp, target):
    """Slides to render for a target: 'live' (HTML in the browser), 'print' (PDF), 'pptx'.
    Adds answer slides for quizzes where the format can't do live feedback, and sources pages
    built from sources[] / credited assets. Hand-written references slides are kept untouched."""
    meta = bp.get("meta", {})
    out, appendix = [], []
    self_read = meta.get("deliveryMode") == "self-read"
    for sl in bp.get("slides", []):
        out.append(sl)
        eng = sl.get("engagement") or {}
        if target in ("print", "pptx") and eng.get("correctOptionId"):
            place = eng.get("answerPlacement") or ("inline" if self_read else "next-slide")
            if place == "next-slide":
                out.append(_answer_slide(bp, sl))
            elif place == "appendix":
                appendix.append(_answer_slide(bp, sl))
    if meta.get("autoSources", True):
        entries = source_entries(bp)
        if entries:
            S = strings(meta.get("language"))
            per = int(meta.get("sourcesPerSlide", 7))
            chunks = [entries[i:i + per] for i in range(0, len(entries), per)]
            for k, ch in enumerate(chunks):
                appendix.append({"id": "_sources_%d" % (k + 1), "role": "references", "dark": False,
                                 "kicker": S["sources"] + ((" · %s %d" % (S["cont"], k + 1)) if k else ""),
                                 "actionTitle": S["sources"], "_entries": ch})
    return out + appendix


# ---------------------------------------------------------------------------------------------
# Charts: one normalised spec so HTML and PPTX show the same values, units and labels
# ---------------------------------------------------------------------------------------------
def _decimals_of(vals):
    d = 0
    for v in vals:
        if isinstance(v, float):
            s = repr(v)
            if "." in s and "e" not in s:
                d = max(d, len(s.split(".")[1].rstrip("0")))
    return min(d, 3)


def chart_spec(data):
    data = data or {}
    kind = data.get("kind", "column")
    if kind not in CHART_KINDS:
        return {"kind": "unsupported", "requested": kind, "data": data}
    series = []
    for s in data.get("series", []) or []:
        series.append({"name": s.get("name", ""), "values": list(s.get("values", []) or []),
                       "points": [list(p) for p in (s.get("points") or [])]})
    allv = [v for s in series for v in s["values"]] + [p[1] for s in series for p in s["points"]]
    dec = data.get("decimals")
    if dec is None:
        dec = _decimals_of(allv)
    hl = data.get("highlight")
    cats = list(data.get("categories", []) or [])
    if isinstance(hl, str) and hl in cats:
        hl = cats.index(hl)
    return {"kind": kind, "categories": cats, "series": series, "unit": data.get("unit", ""),
            "decimals": int(dec), "xLabel": data.get("xLabel", ""), "yLabel": data.get("yLabel", ""),
            "yMin": data.get("yMin"), "highlight": hl if isinstance(hl, int) else None,
            "title": data.get("title", "")}


def fmt_num(v, decimals=0, unit=""):
    try:
        s = ("{:,.%df}" % decimals).format(float(v))
    except (TypeError, ValueError):
        return str(v)
    if unit in ("%", "‰"):
        return s + unit
    return (s + " " + unit) if unit else s


def excel_format(decimals, unit, rtl=False):
    base = "#,##0" + (("." + "0" * decimals) if decimals else "")
    if rtl and unit and re.search(r"[A-Za-z]", unit):
        base = '"%s"' % LRM + base
    if unit:
        base += '"%s%s"' % ("" if unit in ("%", "‰") else " ", unit.replace('"', ""))
    return base


def nice_max(v):
    if v <= 0:
        return 1
    import math
    e = 10 ** math.floor(math.log10(v))
    for m in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if m * e >= v:
            return m * e
    return 10 * e


def nice_ticks(vmax, vmin=0, n=4):
    """Round axis: returns (lo, hi, step) with a 1/2/2.5/5 x 10^k step and ~n intervals."""
    import math
    span = (vmax - vmin) or 1
    raw = span / n
    e = 10 ** math.floor(math.log10(raw))
    step = next(m * e for m in (1, 2, 2.5, 5, 10) if m * e >= raw)
    lo = math.floor(vmin / step) * step
    hi = math.ceil(vmax / step) * step
    return lo, hi, step


def table_from_chart(spec):
    data = spec.get("data") or {}
    cats = data.get("categories", [])
    ser = data.get("series", [])
    return {"columns": [""] + [s.get("name", "") for s in ser],
            "rows": [[c] + [s.get("values", [""] * len(cats))[i] for s in ser] for i, c in enumerate(cats)]}


# ---------------------------------------------------------------------------------------------
# Text sizing: step a title down by length, never below the floor
# ---------------------------------------------------------------------------------------------
def title_scale_for(text):
    n = len(text or "")
    if n <= 48:
        return 1.0
    if n <= 70:
        return 0.86
    if n <= 95:
        return 0.74
    return 0.66


# ---------------------------------------------------------------------------------------------
# Stage merge: apply each stage's output onto the base, but only the fields that stage owns
# ---------------------------------------------------------------------------------------------
OWNERSHIP = {
    "designer": {"top": ["design"], "slide": ["layout", "background", "dark"],
                 "assets": "upsert"},
    "writer": {"meta": ["title", "subtitle"], "slide": ["actionTitle", "kicker", "bullets", "speakerNotes"],
               "exhibit": ["caption"], "engagement": ["prompt", "feedback", "presenterCue"],
               "assetFields": ["alt"]},
    "animator": {"top": ["navigation"], "slide": ["animation"]},
    "engineer": {"top": ["meta", "narrative", "sections", "sources"],
                 "slide": ["role", "section", "exhibit", "engagement", "citations"], "addSlides": True},
}


def merge(base, stage_outputs):
    """merge(base, {"designer": bp_d, "writer": bp_w}) -> new blueprint.
    Each stage may only change the fields it owns (see OWNERSHIP / blueprint-spec.md)."""
    out = copy.deepcopy(base)
    for stage, bp in stage_outputs.items():
        own = OWNERSHIP[stage]
        for k in own.get("top", []):
            if k in bp:
                if k == "meta" and stage == "engineer":
                    keep = {x: out.get("meta", {}).get(x) for x in ("title", "subtitle") if x in out.get("meta", {})}
                    out["meta"] = {**copy.deepcopy(bp["meta"]), **keep}
                else:
                    out[k] = copy.deepcopy(bp[k])
        for k in own.get("meta", []):
            if k in bp.get("meta", {}):
                out.setdefault("meta", {})[k] = bp["meta"][k]
        by = {s.get("id"): s for s in out.get("slides", [])}
        for s in bp.get("slides", []):
            t = by.get(s.get("id"))
            if t is None:
                if own.get("addSlides"):
                    out["slides"].append(copy.deepcopy(s))
                continue
            for k in own.get("slide", []):
                if k in s:
                    t[k] = copy.deepcopy(s[k])
            for k in own.get("exhibit", []):
                if k in (s.get("exhibit") or {}) and t.get("exhibit") is not None:
                    t["exhibit"][k] = s["exhibit"][k]
            for k in own.get("engagement", []):
                if k in (s.get("engagement") or {}) and t.get("engagement") is not None:
                    t["engagement"][k] = copy.deepcopy(s["engagement"][k])
        if own.get("assets") == "upsert" or own.get("assetFields"):
            ab = {a.get("id"): a for a in out.setdefault("assets", [])}
            for a in bp.get("assets", []):
                if a.get("id") in ab:
                    if own.get("assets") == "upsert":
                        alt = ab[a["id"]].get("alt")
                        ab[a["id"]].update(copy.deepcopy(a))
                        if alt is not None:
                            ab[a["id"]]["alt"] = alt
                    for f in own.get("assetFields", []):
                        if f in a:
                            ab[a["id"]][f] = a[f]
                elif own.get("assets") == "upsert":
                    out["assets"].append(copy.deepcopy(a))
    return out
