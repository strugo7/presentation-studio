# -*- coding: utf-8 -*-
"""Generic device frames: shared geometry, HTML (SVG) and PPTX (shapes) output, RTL order, loupe."""
import os
import re
import unittest

from tests.helpers import EXAMPLES, TmpDirMixin, bl, chrome_available, load_json, run_script, write_tmp_blueprint

from pptx import Presentation

DEMO_DIR = os.path.join(EXAMPLES, "product-demo")
DEMO = os.path.join(DEMO_DIR, "demo-he.blueprint.json")


class Geometry(unittest.TestCase):
    def test_screen_keeps_screenshot_aspect(self):
        for dev, ar in (("phone", 0.462), ("laptop", 1.6), ("tablet", 0.75), ("browser", 1.6)):
            scr = bl.device_geometry(dev, ar)["screen"]
            self.assertAlmostEqual(scr["w"] / scr["h"], ar, places=3, msg=dev)

    def test_out_of_range_aspect_is_clamped(self):
        scr = bl.device_geometry("phone", 1.6)["screen"]          # landscape shot in a phone: letterboxed
        self.assertLessEqual(scr["w"] / scr["h"], bl.DEVICE_AR["phone"][1] + 1e-9)

    def test_row_order_flips_in_rtl_and_overlap_overlaps(self):
        items = [{"device": "laptop", "ar": 1.6, "ref": "a"}, {"device": "phone", "ar": 0.46, "ref": "b"}]
        _, _, ltr = bl.device_row(items, rtl=False)
        _, _, rtl = bl.device_row(items, rtl=True)
        self.assertEqual([p[0]["ref"] for p in ltr], ["a", "b"])
        self.assertEqual([p[0]["ref"] for p in rtl], ["b", "a"])  # drawn left to right: first item ends up on the right
        W, H, ov = bl.device_row(items, rtl=True, arrangement="overlap")
        (_, ga, xa, _, sa), (_, gb, xb, _, sb) = ov
        self.assertLess(xb, xa + ga["W"] * sa)                     # phone starts inside the laptop...
        self.assertGreater(xb + gb["W"] * sb, xa + ga["W"] * sa)   # ...and sticks out past its right (start) edge

    def test_loupe_stays_on_screen(self):
        g = bl.device_geometry("laptop", 1.6)
        lp = bl.loupe_geometry(g["screen"], 1.6, {"x": 0.95, "y": 0.0, "w": 0.2, "h": 0.2})
        s = g["screen"]
        self.assertGreaterEqual(lp["cx"] - lp["d"] / 2, s["x"] - 1e-9)
        self.assertLessEqual(lp["cx"] + lp["d"] / 2, s["x"] + s["w"] + 1e-9)
        self.assertTrue(all(c >= -1e-9 for c in lp["crop"]))      # the window never leaves the image


class Validation(TmpDirMixin, unittest.TestCase):
    def test_refs_checked_and_misuse_warned(self):
        bp = {"meta": {"title": "t"}, "slides": [
            {"id": "a", "exhibit": {"type": "screenshot", "devices": [{"device": "phone", "ref": "nope"}]}},
            {"id": "b", "exhibit": {"type": "chart", "device": "phone", "data": {"kind": "column", "unit": "%",
                                                                                  "categories": ["x"], "series": [{"name": "s", "values": [1]}]}}}]}
        errors, warnings = bl.validate(bl.normalise(bp))
        self.assertTrue(any("devices[0].ref" in e for e in errors), errors)
        self.assertTrue(any("only frame screenshots" in w for w in warnings), warnings)

    def test_example_valid_and_cited(self):
        bp = bl.load(DEMO)
        self.assertEqual(bl.validate(bp, DEMO_DIR)[0], [])
        for s in bp["slides"]:
            if s["role"] not in ("cover",):
                self.assertTrue(s.get("citations"), s["id"])


class Render(TmpDirMixin, unittest.TestCase):
    def test_html(self):
        out = os.path.join(self.tmp, "h")
        run_script("render_html.py", DEMO, out, DEMO_DIR)
        with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
            h = f.read()
        svgs = re.findall(r'<svg class="device-svg".*?</svg>', h, flags=re.S)
        self.assertEqual(len(svgs), 5)                        # laptop, phone, pair, together, try
        self.assertTrue(all('preserveAspectRatio="xMidYMid meet" clip-path' in s for s in svgs))  # never cropped
        self.assertEqual(sum(s.count('class="loupe"') for s in svgs), 1)
        pair = next(s for s in svgs if "iOS" in s)
        x = {lab: float(re.search(r'<text x="([\d.]+)"[^>]*class="dv-l">%s<' % lab, pair).group(1)) for lab in ("iOS", "Android")}
        self.assertGreater(x["iOS"], x["Android"])                  # RTL: first device on the right
        self.assertIn('direction="ltr">app.pinkas.example/close<', h)
        self.assertNotIn("scaleX(-1)", h)                          # nothing mirrored

    def test_pptx(self):
        out = os.path.join(self.tmp, "d.pptx")
        run_script("render_pptx.py", DEMO, out, DEMO_DIR)
        prs = Presentation(out)
        ids = [s["id"] for s in bl.expand_slides(bl.load(DEMO), "pptx")]
        pics = lambda sid: [sh for sh in prs.slides[ids.index(sid)].shapes if sh.shape_type == 13]
        self.assertEqual(len(pics("pair")), 2)
        self.assertEqual(len(pics("laptop")), 2)                    # screen + loupe
        geoms = [p._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom").get("prst") for p in pics("laptop")]
        self.assertIn("ellipse", geoms)
        phone_geom = pics("phone")[0]._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom").get("prst")
        self.assertEqual(phone_geom, "roundRect")                   # rounded screen corners
        descr = pics("phone")[0]._element.nvPicPr.cNvPr.get("descr")
        self.assertIn("212", descr)

    def test_old_blueprint_unchanged(self):
        bp = load_json(os.path.join(EXAMPLES, "sample-blueprint.json"))
        self.assertFalse(any(bl.exhibit_devices(s.get("exhibit")) for s in bp["slides"]))


if __name__ == "__main__":
    unittest.main()


@unittest.skipUnless(chrome_available(), "chrome not available")
class PDFNeverStale(TmpDirMixin, unittest.TestCase):
    def test_old_pdf_is_replaced(self):
        out = os.path.join(self.tmp, "deck.pdf")
        with open(out, "wb") as f:
            f.write(b"%PDF-1.4 stale file from an earlier build")
        run_script("render_pdf.py", DEMO, out, DEMO_DIR, timeout=300)
        with open(out, "rb") as f:
            data = f.read()
        self.assertNotIn(b"stale file", data)
        self.assertGreater(len(data), 100000)
