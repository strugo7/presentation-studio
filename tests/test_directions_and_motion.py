# -*- coding: utf-8 -*-
"""Direction previews (same blueprint, 2-3 systems side by side), chart colours that stay distinct in
every system, and motion behaviour that the docs promise (PPTX transitions; HTML ignores them)."""
import json
import os
import re
import subprocess
import sys
import unittest
import zipfile

from tests.helpers import (EXAMPLES, SHARED, TmpDirMixin, bl, load_json, node_playwright_available, run_script,
                           write_tmp_blueprint)

from pptx import Presentation

MIXED = os.path.join(EXAMPLES, "mixed-sources")
EXEC = os.path.join(MIXED, "exec-he.blueprint.json")


def visible_text(html_doc):
    """Text inside the slides only (no attributes, styles or scripts)."""
    body = "".join(re.findall(r"<section class=\"slide.*?</section>", html_doc, flags=re.S))
    body = re.sub(r"<aside class=\"notes\">.*?</aside>", "", body, flags=re.S)
    return re.sub(r"<[^>]+>", " ", body)


class DirectionPreviews(TmpDirMixin, unittest.TestCase):
    def preview(self, *extra):
        out = os.path.join(self.tmp, "prev")
        p = subprocess.run([sys.executable, os.path.join(SHARED, "preview_directions.py"), EXEC, out, MIXED] + list(extra),
                           capture_output=True, text=True, timeout=240)
        return p, out

    def test_two_directions_same_content(self):
        p, out = self.preview("--systems=executive-data-briefing,swiss")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("slides: cover,trend", p.stdout)           # cover + the first real chart, not the big number
        with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
            page = f.read()
        self.assertIn("executive-data-briefing", page)
        self.assertIn("swiss", page)
        docs = {}
        for system in ("executive-data-briefing", "swiss"):
            for sid in ("cover", "trend"):
                path = os.path.join(out, system, sid, "index.html")
                self.assertTrue(os.path.exists(path), path)
                with open(path, encoding="utf-8") as f:
                    docs[(system, sid)] = f.read()
        # same words on both directions' slides, no direction label inside a slide
        for sid in ("cover", "trend"):
            a, b = visible_text(docs[("executive-data-briefing", sid)]), visible_text(docs[("swiss", sid)])
            self.assertIn("עובדים", a + b)
            for label in ("swiss", "executive-data-briefing", "preview", "Direction"):
                self.assertNotIn(label, a)
                self.assertNotIn(label, b)
        # the design actually differs (system class, motif), not just the file name
        self.assertIn("sys-signal", docs[("executive-data-briefing", "trend")])
        self.assertIn("sys-swiss", docs[("swiss", "trend")])
        self.assertIn("motif-rule", docs[("executive-data-briefing", "trend")])
        self.assertIn("motif-numbers", docs[("swiss", "trend")])
        # every reveal is shown in a preview (no data-step left)
        self.assertNotIn("data-step=", docs[("swiss", "trend")])
        # the source blueprint is untouched
        self.assertEqual(load_json(EXEC)["design"]["system"], "executive-data-briefing")

    def test_explicit_slides_and_validation(self):
        p, _ = self.preview("--systems=keynote,technical-case", "--slides=options,dash")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("slides: cover,options,dash", p.stdout)
        bad, _ = self.preview("--systems=keynote,neon-cyber")
        self.assertEqual(bad.returncode, 2)
        self.assertIn("unknown design system", bad.stdout)
        one, _ = self.preview("--systems=keynote")
        self.assertEqual(one.returncode, 2)

    @unittest.skipUnless(node_playwright_available(), "node + playwright not available")
    def test_png(self):
        p, out = self.preview("--systems=classroom-workshop,keynote", "--png")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("png: True", p.stdout)
        for system in ("classroom-workshop", "keynote"):
            self.assertTrue(os.path.getsize(os.path.join(out, system, "cover.png")) > 10000)


class ChartColours(TmpDirMixin, unittest.TestCase):
    def test_series_distinct_in_every_system(self):
        for name in list(bl.SYSTEM_TOKENS) + list(bl.SYSTEM_ALIASES):
            ser, hl, base = bl.chart_colors(bl.palette({"system": name}))
            self.assertEqual(len(set(ser)), 4, name)
            self.assertNotEqual(hl, base, name)

    def two_series_bp(self, system, kind="column"):
        return {"meta": {"title": "t", "language": "en"}, "design": {"system": system},
                "slides": [{"id": "c", "role": "evidence", "layout": "full-exhibit", "actionTitle": "Two series",
                            "exhibit": {"type": "chart", "data": {"kind": kind, "unit": "%", "categories": ["A", "B", "C"],
                                                                  "series": [{"name": "x", "values": [1, 2, 3]},
                                                                             {"name": "y", "values": [3, 2, 1]}]}}}]}

    def test_swiss_two_series_html_and_pptx(self):
        path = write_tmp_blueprint(self.two_series_bp("swiss"), self.tmp)
        out = os.path.join(self.tmp, "h")
        run_script("render_html.py", path, out)
        with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
            svg = re.search(r"<svg class=\"chart-svg\".*?</svg>", f.read(), flags=re.S).group(0)
        fills = set(re.findall(r'<rect x="[^"]+" y="[^"]+" width="[^"]+" height="[^"]+" rx="6" fill="#([0-9A-F]{6})"', svg))
        self.assertEqual(len(fills), 2, fills)
        run_script("render_pptx.py", path, os.path.join(self.tmp, "d.pptx"))
        prs = Presentation(os.path.join(self.tmp, "d.pptx"))
        chart = next(sh.chart for sh in prs.slides[0].shapes if sh.has_chart)
        cols = {str(s.format.fill.fore_color.rgb) for s in chart.series}
        self.assertEqual(len(cols), 2, cols)

    def test_bar_chart_unit_label_not_over_categories(self):
        bp = self.two_series_bp("signal", "bar")
        path = write_tmp_blueprint(bp, self.tmp)
        out = os.path.join(self.tmp, "h")
        run_script("render_html.py", path, out)
        with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
            svg = re.search(r"<svg class=\"chart-svg\".*?</svg>", f.read(), flags=re.S).group(0)
        self.assertNotIn("rotate(-90", svg)          # no rotated label on the category column
        bp["slides"][0]["exhibit"]["data"]["yLabel"] = "share of respondents"
        path = write_tmp_blueprint(bp, self.tmp, "b2.json")
        run_script("render_html.py", path, out)
        with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
            svg = re.search(r"<svg class=\"chart-svg\".*?</svg>", f.read(), flags=re.S).group(0)
        self.assertIn('class="ax-v">share of respondents</text>', svg)


class MotionMatchesDocs(TmpDirMixin, unittest.TestCase):
    """format-capabilities.md: PPTX maps transitions; HTML ignores them (camera flight); reveal zoom unused."""
    def bp(self):
        mk = lambda i, tr: {"id": "s%d" % i, "role": "concept", "actionTitle": "Slide %d" % i,
                            **({"animation": {"transition": tr}} if tr else {})}
        return {"meta": {"title": "t", "language": "en"},
                "slides": [mk(1, None), mk(2, "morph"), mk(3, "fade"), mk(4, "push"), mk(5, "none")]}

    def test_pptx_transitions(self):
        path = write_tmp_blueprint(self.bp(), self.tmp)
        out = os.path.join(self.tmp, "d.pptx")
        run_script("render_pptx.py", path, out)
        with zipfile.ZipFile(out) as z:
            xml = {i: z.read("ppt/slides/slide%d.xml" % i).decode("utf-8") for i in range(1, 6)}
        self.assertNotIn("transition", xml[1])
        self.assertIn("p159:morph", xml[2])
        self.assertIn("<p:fade/>", xml[2])                # fallback for apps without Morph
        self.assertIn("<p:fade/>", xml[3])
        self.assertIn("<p:fade/>", xml[4])                # push is built as a fade
        self.assertNotIn("push", xml[4])
        self.assertNotIn("transition", xml[5])
        # shared names so Morph matches titles across slides
        prs = Presentation(out)
        self.assertTrue(all(any(sh.name == "!!title" for sh in s.shapes) for s in prs.slides))

    def test_html_ignores_transition_and_reveal_zoom(self):
        bp = self.bp()
        bp["slides"][1]["animation"]["reveals"] = [{"step": 1, "show": ["title"], "zoom": "annotate"}]
        path = write_tmp_blueprint(bp, self.tmp)
        out = os.path.join(self.tmp, "h")
        run_script("render_html.py", path, out)
        with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
            h = f.read()
        self.assertNotIn("morph", h.lower())
        self.assertNotIn("data-zoom", h)
        self.assertIn('data-step="1"', h)                 # the reveal itself is built
        self.assertIn('id="count" dir="ltr"', h)          # "1 / 5" never flips to "5 / 1" in RTL decks


class NumeralClearsTitle(TmpDirMixin, unittest.TestCase):
    def test_swiss_section_numeral_does_not_overlap_title(self):
        bp = load_json(EXEC)
        bp["design"] = {"system": "swiss"}
        bp["sections"] = [{"id": "sec1", "title": "A", "slideIds": [s["id"] for s in bp["slides"]]}]
        path = write_tmp_blueprint(bp, self.tmp)
        out = os.path.join(self.tmp, "d.pptx")
        run_script("render_pptx.py", path, out, MIXED)
        prs = Presentation(out)
        checked = 0
        for s in prs.slides:
            num = next((sh for sh in s.shapes if sh.name == "!!secnum"), None)
            title = next((sh for sh in s.shapes if sh.name == "!!title"), None)
            if num is None or title is None:
                continue
            checked += 1
            a = (num.left, num.top, num.width, num.height)
            b = (title.left, title.top, title.width, title.height)
            self.assertTrue(a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1],
                            "section numeral overlaps the title")
        self.assertGreater(checked, 0)


if __name__ == "__main__":
    unittest.main()
