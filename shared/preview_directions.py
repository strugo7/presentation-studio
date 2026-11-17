# -*- coding: utf-8 -*-
"""Render 2-3 visual directions of the SAME blueprint side by side, before the full deck is built.

For each design system it renders the cover plus one or two typical slides (a chart, a diagram, a
product screen...) from the user's own content, with every reveal shown, and writes a comparison page.
Nothing in the blueprint contract changes: the script works on temporary copies and only sets
design.system on each copy.

Usage:
  python preview_directions.py blueprint.json out_dir [assets_dir]
         --systems=executive-data-briefing,swiss,editorial-report
         [--slides=id1,id2]   slides to show after the cover (default: auto-pick one typical slide)
         [--keep-brand]       keep the blueprint's own design.palette / design.tokens in every direction
         [--png]              also write PNG screenshots (needs node + playwright; skipped otherwise)
         [--font=path.ttf]    passed through to render_html.py

Output: out_dir/index.html (open it), out_dir/<system>/<slide-id>/index.html, and PNGs with --png.
Direction names appear only in the comparison page, never on a slide.
"""
import copy, html, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import blueprint_lib as bl  # noqa: E402

E = html.escape
# Exhibit types in the order we prefer them as "the typical slide" of a deck.
TYPICAL_ORDER = ("chart", "diagram", "screenshot", "image", "table", "big-number", "code")
TOKEN_KEYS = ("titleScale", "titleWeight", "coverAlign", "motif", "frame", "margin", "kicker", "radius")


def known_systems():
    return set(bl.SYSTEM_TOKENS) | set(bl.SYSTEM_ALIASES)


def exhibit_kind(slide):
    """What job the slide's exhibit does: a big-number slide is not a chart, even if typed as one."""
    ex = slide.get("exhibit") or {}
    if slide.get("layout") == "big-number" or ex.get("bigNumber"):
        return "big-number"
    if ex.get("type") == "chart" and not ex.get("data"):
        return None
    return ex.get("type")


def pick_slides(bp, wanted=None):
    """Return [cover, typical...] slide dicts from the blueprint."""
    slides = bp.get("slides", [])
    if not slides:
        raise SystemExit("blueprint has no slides")
    cover = next((s for s in slides if s.get("role") == "cover"), slides[0])
    if wanted:
        by_id = {s.get("id"): s for s in slides}
        missing = [w for w in wanted if w not in by_id]
        if missing:
            raise SystemExit("unknown slide id(s): " + ", ".join(missing))
        rest = [by_id[w] for w in wanted if by_id[w] is not cover]
    else:
        rest = []
        for t in TYPICAL_ORDER:
            hit = next((s for s in slides if s is not cover and exhibit_kind(s) == t), None)
            if hit:
                rest = [hit]
                break
        if not rest:  # no exhibit anywhere: show the first content slide
            rest = [s for s in slides if s is not cover][:1]
    return [cover] + rest


def direction_blueprint(bp, system, slide, keep_brand=False):
    """One-slide copy of the blueprint in a given design system, with all reveals shown."""
    b = copy.deepcopy(bp)
    design = b.setdefault("design", {})
    design["system"] = system
    if not keep_brand:
        for k in ("palette", "tokens", "gridBackground", "variant", "motif"):
            design.pop(k, None)
    s = copy.deepcopy(slide)
    s.pop("animation", None)  # every element visible: a preview is judged in its final state
    b["slides"] = [s]
    b.setdefault("meta", {})["autoSources"] = False
    b["navigation"] = {"mode": "linear"}
    return b


def token_summary(system, keep_design=None):
    _, tok = bl.resolve_system(dict(keep_design or {}, system=system))
    pal = bl.palette(dict(keep_design or {}, system=system))
    return tok, pal


def screenshot(jobs):
    """jobs: [(html_path, png_path)]. Returns True if PNGs were written."""
    if not shutil.which("node"):
        return False
    js = r"""
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[1]);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const [src, dst] of jobs) {
    await p.goto('file://' + src);
    await p.addStyleTag({ content: '.hud{display:none!important}' });
    await p.evaluate(() => document.fonts ? document.fonts.ready : null);
    await p.waitForTimeout(500);
    await p.screenshot({ path: dst });
  }
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
"""
    r = subprocess.run(["node", "-e", js, json.dumps(jobs)], capture_output=True, text=True)
    if r.returncode != 0:
        print("warning: PNG step skipped:", (r.stderr or r.stdout).strip().splitlines()[-1:] or "")
        return False
    return True


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    flags = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else True) for a in argv if a.startswith("--")}
    if len(args) < 2 or "--systems" not in flags:
        print(__doc__)
        return 2
    src, out = args[0], os.path.abspath(args[1])
    assets = args[2] if len(args) > 2 else os.path.dirname(os.path.abspath(src))
    systems = [s.strip() for s in str(flags["--systems"]).split(",") if s.strip()]
    unknown = [s for s in systems if s not in known_systems()]
    if unknown:
        print("unknown design system(s): %s\nknown: %s" % (", ".join(unknown), ", ".join(sorted(known_systems()))))
        return 2
    if not 2 <= len(systems) <= 4:
        print("give 2-3 directions (4 at most) so the choice stays readable")
        return 2
    keep = bool(flags.get("--keep-brand"))
    wanted = [w for w in str(flags.get("--slides", "")).split(",") if w] if flags.get("--slides") else None

    bp = bl.load(src)
    chosen = pick_slides(bp, wanted)
    os.makedirs(out, exist_ok=True)
    render = os.path.join(HERE, "render_html.py")
    extra = ["--font=" + flags["--font"]] if isinstance(flags.get("--font"), str) else []

    cells, jobs = {}, []
    tmp = os.path.join(out, "_blueprints")
    os.makedirs(tmp, exist_ok=True)
    for system in systems:
        for sl in chosen:
            sid = sl.get("id") or "slide"
            b = direction_blueprint(bp, system, sl, keep)
            bpath = os.path.join(tmp, "%s__%s.json" % (system, sid))
            with open(bpath, "w", encoding="utf-8") as f:
                json.dump(b, f, ensure_ascii=False)
            dst = os.path.join(out, system, sid)
            r = subprocess.run([sys.executable, render, bpath, dst, assets] + extra, capture_output=True, text=True)
            if r.returncode != 0:
                print(r.stdout, r.stderr)
                return 1
            for line in r.stdout.splitlines():
                if line.startswith("warning:"):
                    print("%s/%s %s" % (system, sid, line))
            cells[(system, sid)] = os.path.join(dst, "index.html")
            jobs.append((cells[(system, sid)], os.path.join(out, system, sid + ".png")))

    have_png = bool(flags.get("--png")) and screenshot(jobs)

    meta = bp.get("meta", {})
    rows = []
    for system in systems:
        tok, pal = token_summary(system, bp.get("design") if keep else None)
        base = bl.SYSTEM_ALIASES[system][0] if system in bl.SYSTEM_ALIASES else system
        facts = " · ".join("%s %s" % (k, tok.get(k)) for k in TOKEN_KEYS)
        sw = "".join('<span class="sw" style="background:#%s" title="%s #%s"></span>' % (pal[k], k, pal[k])
                     for k in ("dark", "accent", "accent2", "ink", "bgAlt"))
        figs = []
        for sl in chosen:
            sid = sl.get("id") or "slide"
            rel = os.path.relpath(cells[(system, sid)], out)
            if have_png:
                inner = '<img src="%s/%s.png" alt="%s: %s" loading="lazy">' % (E(system), E(sid), E(system), E(sl.get("actionTitle", sid)))
            else:
                inner = '<iframe src="%s" title="%s: %s" loading="lazy" tabindex="-1"></iframe>' % (E(rel), E(system), E(sid))
            figs.append('<figure><a href="%s">%s</a><figcaption>%s</figcaption></figure>' % (E(rel), inner, E(sid)))
        rows.append('<section><h2>%s <small>%s</small></h2><p class="tok">%s %s</p><div class="row">%s</div></section>'
                    % (E(system), ("based on " + E(base)) if base != system else "preset", sw, E(facts), "".join(figs)))
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Direction previews: %s</title>
<style>body{font:16px/1.45 system-ui,sans-serif;margin:32px;color:#1a2230;background:#f4f5f7}h1{font-size:22px;margin:0 0 4px}
.lead{color:#5b6472;margin:0 0 24px}section{background:#fff;border:1px solid #e2e5ea;border-radius:10px;padding:18px 20px;margin:0 0 20px}
h2{font-size:18px;margin:0}h2 small{font-weight:400;color:#5b6472;font-size:14px;margin-inline-start:8px}.tok{color:#5b6472;font-size:13px;margin:6px 0 12px}
.sw{display:inline-block;width:14px;height:14px;border-radius:3px;margin-inline-end:3px;vertical-align:-2px;border:1px solid #0002}
.row{display:grid;grid-template-columns:repeat(%d,1fr);gap:14px}figure{margin:0}figure a{display:block;aspect-ratio:16/9;border:1px solid #e2e5ea;overflow:hidden;background:#fff}
figure img,figure iframe{width:100%%;height:100%%;border:0;display:block}figure iframe{pointer-events:none}figcaption{font-size:12px;color:#5b6472;margin-top:4px}</style></head><body>
<h1>%s</h1><p class="lead">The same slides in %d directions. Compare composition, density and title size, not only colour. Click a slide to open it full size.</p>
%s</body></html>""" % (E(meta.get("title", "")), len(chosen), E(meta.get("title", "Direction previews")), len(systems), "\n".join(rows))
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    shutil.rmtree(tmp, ignore_errors=True)
    print("saved", os.path.join(out, "index.html"), "| directions:", ",".join(systems),
          "| slides:", ",".join(s.get("id", "?") for s in chosen), "| png:", have_png)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
