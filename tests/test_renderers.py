# -*- coding: utf-8 -*-
"""Renderer tests: HTML + PPTX output for the old sample (backward compatibility) and the features
fixture, chart parity between formats, interaction (Playwright, if present) and PDF (Chrome, if present)."""
import json
import os
import re
import shutil
import subprocess
import unittest

from tests.helpers import (EXAMPLES, FEATURES, ROOT, SAMPLE, TmpDirMixin, bl, chrome_available, load_json,
                           node_playwright_available, run_script, write_tmp_blueprint)

from pptx import Presentation
from pptx.enum.chart import XL_CHART_TYPE


def boxes_overlap(a, b):
    return not (a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1])


class HTMLRender(TmpDirMixin, unittest.TestCase):
    def render(self, bp, *extra):
        out = os.path.join(self.tmp, "html")
        run_script("render_html.py", bp, out, EXAMPLES, *extra)
        with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
            return out, f.read()

    def test_sample_renders_offline(self):
        _, h = self.render(SAMPLE)
        self.assertEqual(h.count('class="slide '), 6)
        self.assertNotIn("fonts.googleapis.com", h)
        self.assertIn("@font-face", h)

    def test_features_layouts_and_engagement(self):
        out, h = self.render(FEATURES)
        for lay in ("lay-statement", "lay-split", "lay-full-exhibit", "lay-big-number"):
            self.assertIn(lay, h)
        self.assertIn('role="radiogroup"', h)
        self.assertIn('data-mode="quiz"', h)
        self.assertIn('data-mode="poll"', h)
        self.assertIn('class="seq-svg"', h)
        self.assertIn("prefers-reduced-motion", h)
        self.assertIn('rel="noopener noreferrer"', h)
        self.assertIn("<cite>", h)
        files = sorted(os.listdir(os.path.join(out, "assets")))
        self.assertEqual(len([f for f in files if f.startswith("dash_")]), 2, files)

    def test_line_chart_is_a_line(self):
        _, h = self.render(FEATURES)
        svg = re.search(r'<svg class="chart-svg" data-kind="line".*?</svg>', h, re.S).group(0)
        self.assertEqual(svg.count("<polyline"), 2)
        self.assertIn("96.3 ms", svg)
        self.assertIn("TLS 1.3", svg)

    def test_print_build_has_answers(self):
        _, h = self.render(FEATURES, "--pdf")
        self.assertIn('id="s-quiz__answer"', h)
        self.assertIn('id="s-_sources_1"', h)


class PPTXRender(TmpDirMixin, unittest.TestCase):
    def render(self, bp):
        out = os.path.join(self.tmp, "deck.pptx")
        log = run_script("render_pptx.py", bp, out, EXAMPLES)
        return Presentation(out), log

    def test_sample_backward_compatible_no_overlaps(self):
        prs, _ = self.render(SAMPLE)
        self.assertEqual(len(prs.slides), 6)
        for i, s in enumerate(prs.slides, 1):
            boxes = [(sh.left, sh.top, sh.width, sh.height, sh.text_frame.text[:30]) for sh in s.shapes
                     if sh.has_text_frame and sh.text_frame.text.strip()]
            for a in range(len(boxes)):
                for b in range(a + 1, len(boxes)):
                    self.assertFalse(boxes_overlap(boxes[a][:4], boxes[b][:4]),
                                     "slide %d: %r overlaps %r" % (i, boxes[a][4], boxes[b][4]))

    def test_features_charts_links_citations(self):
        prs, log = self.render(FEATURES)
        bp = bl.load(FEATURES)
        ids = [s["id"] for s in bl.expand_slides(bp, "pptx")]
        self.assertEqual(len(prs.slides), len(ids))
        charts = [sh.chart for s in prs.slides for sh in s.shapes if sh.has_chart]
        line = next(c for c in charts if c.chart_type == XL_CHART_TYPE.LINE_MARKERS)
        self.assertEqual([s.name for s in line.series], ["TLS 1.2", "TLS 1.3"])
        self.assertEqual(list(line.plots[0].categories), ["שבוע 1", "שבוע 2", "שבוע 3", "שבוע 4"])
        self.assertAlmostEqual(list(line.series[1].values)[-1], 96.3)
        self.assertTrue(line.value_axis.has_title)
        # quiz options hyperlink to the generated answer slide
        quiz = prs.slides[ids.index("quiz")]
        answer = prs.slides[ids.index("quiz__answer")]
        targets = [sh.click_action.target_slide for sh in quiz.shapes if sh.name.startswith("s") and sh.click_action.target_slide is not None]
        self.assertTrue(targets and all(t == answer for t in targets))
        # citation in the slide foot, presenter cue in notes, sources slide with a link
        text = " ".join(sh.text_frame.text for sh in prs.slides[ids.index("seq")].shapes if sh.has_text_frame)
        self.assertIn("RFC 8446", text)
        self.assertIn("תנו לחדר לבחור", quiz.notes_slide.notes_text_frame.text)
        src = prs.slides[ids.index("_sources_1")]
        links = [r.hyperlink.address for sh in src.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs for r in p.runs if r.hyperlink.address]
        self.assertIn("https://www.rfc-editor.org/rfc/rfc8446", links)
        # alt text on pictures, and the SVG-only asset degrades with a warning instead of crashing
        descrs = [sh._element.nvPicPr.cNvPr.get("descr") for s in prs.slides for sh in s.shapes if sh.shape_type == 13]
        self.assertIn("לוח מדידות עם עמודות latency לפני השינוי", descrs)
        self.assertIn("flow_nofb", log)

    def test_two_systems_differ_on_same_content(self):
        bp = load_json(SAMPLE)
        res = {}
        for sysname in ("cobalt-grid", "editorial"):
            bp["design"]["system"] = sysname
            bp["design"].pop("palette", None)
            path = write_tmp_blueprint(bp, self.tmp, sysname + ".json")
            prs, _ = self.render(path)
            title = next(sh for sh in prs.slides[3].shapes if sh.name == "!!title")
            res[sysname] = (title.left, title.text_frame.paragraphs[0].runs[0].font.size, title.text_frame.paragraphs[0].runs[0].font.bold)
        self.assertNotEqual(res["cobalt-grid"], res["editorial"])


@unittest.skipUnless(node_playwright_available(), "node + playwright not available")
class HTMLInteraction(TmpDirMixin, unittest.TestCase):
    def test_quiz_keys_feedback_reduced_motion_offline(self):
        out = os.path.join(self.tmp, "html")
        run_script("render_html.py", FEATURES, out, EXAMPLES)
        p = subprocess.run(["node", os.path.join(ROOT, "tests", "js", "interaction_check.js"),
                            os.path.join(out, "index.html"), "quiz", "poll"], capture_output=True, text=True, timeout=120)
        r = json.loads(p.stdout.strip().splitlines()[-1])
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["afterEnterIdx"], r["quizIdx"])          # Enter on an option didn't advance
        self.assertEqual(r["afterSpaceIdx"], r["quizIdx"])
        self.assertIn("ServerHello", r["wrongFeedback"])
        self.assertIn("no", r["wrongClass"])
        self.assertEqual(r["focusMoved"], "c")                      # arrows move between options
        self.assertEqual(r["rightChecked"], "true")
        self.assertEqual(r["correctMarked"], "a")
        self.assertIn("ClientHello", r["revealFeedback"])
        self.assertEqual(r["pollCounts"], ["2", "1"])
        self.assertEqual(r["arrowIdx"], 1)                          # deck keys work outside the quiz
        self.assertFalse(r["rmDefault"])
        self.assertTrue(r["rmReduce"])
        self.assertEqual(r["externalRequests"], [])


@unittest.skipUnless(chrome_available() and shutil.which("pdftotext"), "chrome or pdftotext not available")
class PDFRender(TmpDirMixin, unittest.TestCase):
    def test_pdf_has_all_steps_answers_sources(self):
        out = os.path.join(self.tmp, "deck.pdf")
        run_script("render_pdf.py", FEATURES, out, EXAMPLES, timeout=300)
        txt = subprocess.run(["pdftotext", out, "-"], capture_output=True, text=True).stdout
        n = len(bl.expand_slides(bl.load(FEATURES), "print"))
        pages = subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout
        self.assertIn("Pages:           %d" % n, pages)
        self.assertIn("המדידה כוללת רק חיבורים חדשים", txt)   # a step-2 reveal is printed
        self.assertIn("key_share", txt)                          # answer slide
        self.assertIn("RFC 8446", txt)                           # sources page


MIXED = os.path.join(EXAMPLES, "mixed-sources")


class MixedSourcesDecks(TmpDirMixin, unittest.TestCase):
    """Two decks from one source set must share facts but differ in structure, evidence and direction."""
    def setUp(self):
        super().setUp()
        self.stu = bl.load(os.path.join(MIXED, "students-he.blueprint.json"))
        self.exe = bl.load(os.path.join(MIXED, "exec-he.blueprint.json"))

    def test_same_sources_valid(self):
        self.assertEqual(self.stu["sources"], self.exe["sources"])
        for bp in (self.stu, self.exe):
            self.assertEqual(bl.validate(bp, MIXED)[0], [])

    def test_every_fact_slide_cites(self):
        for bp in (self.stu, self.exe):
            for s in bp["slides"]:
                if s.get("exhibit", {}).get("type") in ("chart", "table") or s.get("layout") == "big-number":
                    self.assertTrue(s.get("citations"), s["id"])

    def test_decks_differ(self):
        lay = lambda bp: [s.get("layout") or s["role"] for s in bp["slides"]]
        self.assertNotEqual(lay(self.stu), lay(self.exe))
        self.assertNotEqual(bl.resolve_system(self.stu["design"])[0], bl.resolve_system(self.exe["design"])[0])
        self.assertTrue(any(s.get("engagement", {}).get("type") == "quiz" for s in self.stu["slides"]))
        self.assertFalse(any(s.get("engagement", {}).get("type") == "quiz" for s in self.exe["slides"]))
        self.assertEqual(self.exe["slides"][1]["layout"], "statement")        # decision first
        self.assertEqual(self.stu["slides"][1].get("engagement", {}).get("type"), "question")  # question first

    def test_both_render(self):
        for name in ("students-he", "exec-he"):
            run_script("render_html.py", os.path.join(MIXED, name + ".blueprint.json"), os.path.join(self.tmp, name), MIXED)
            run_script("render_pptx.py", os.path.join(MIXED, name + ".blueprint.json"), os.path.join(self.tmp, name + ".pptx"), MIXED)


if __name__ == "__main__":
    unittest.main()
