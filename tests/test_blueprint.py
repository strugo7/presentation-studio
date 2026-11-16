# -*- coding: utf-8 -*-
"""Contract tests: schema, backward compatibility, cross-references, assets, merge, charts."""
import copy
import os
import unittest

from tests.helpers import FEATURES, SAMPLE, EXAMPLES, TmpDirMixin, bl, load_json


class SchemaAndRefs(unittest.TestCase):
    def test_sample_still_valid(self):
        errors, _ = bl.validate(bl.load(SAMPLE), EXAMPLES)
        self.assertEqual(errors, [])

    def test_features_valid(self):
        errors, _ = bl.validate(bl.load(FEATURES), EXAMPLES)
        self.assertEqual(errors, [])

    def test_old_blueprint_normalises(self):
        bp = bl.load(SAMPLE)
        self.assertEqual(bp["meta"]["audience"]["profile"], "L&D team")  # who -> profile
        self.assertEqual(bp["sources"], [])
        self.assertEqual(len(bl.expand_slides(bp, "pptx")), 6)  # no sources -> no generated slides

    def _broken(self, mutate):
        bp = load_json(FEATURES)
        mutate(bp)
        return bl.validate(bl.normalise(bp), EXAMPLES)[0]

    def test_unknown_source_id(self):
        errs = self._broken(lambda bp: bp["slides"][1]["citations"].__setitem__(0, {"sourceId": "nope"}))
        self.assertTrue(any("nope" in e for e in errs), errs)

    def test_wrong_correct_option(self):
        def m(bp):
            next(s for s in bp["slides"] if s["id"] == "quiz")["engagement"]["correctOptionId"] = "z"
        self.assertTrue(any("correctOptionId" in e for e in self._broken(m)))

    def test_unknown_asset_id(self):
        def m(bp):
            next(s for s in bp["slides"] if s["id"] == "screens")["exhibit"]["ref"] = "missing_asset"
        self.assertTrue(any("missing_asset" in e for e in self._broken(m)))

    def test_section_reference(self):
        self.assertTrue(any("ghost" in e for e in self._broken(lambda bp: bp["sections"][0]["slideIds"].append("ghost"))))

    def test_chart_length_mismatch(self):
        def m(bp):
            next(s for s in bp["slides"] if s["id"] == "trend")["exhibit"]["data"]["series"][0]["values"].pop()
        self.assertTrue(any("values for" in e for e in self._broken(m)))

    def test_unsafe_url_rejected(self):
        self.assertTrue(any("http" in e for e in self._broken(lambda bp: bp["sources"][0].__setitem__("url", "javascript:alert(1)"))))


class Assets(TmpDirMixin, unittest.TestCase):
    def test_same_basename_two_files(self):
        bp = bl.load(FEATURES)
        A = bl.Assets(bp, EXAMPLES)
        a, b = A.file_for("dash_a"), A.file_for("dash_b")
        self.assertEqual(os.path.basename(a), os.path.basename(b))
        self.assertNotEqual(A.dest_name("dash_a", a), A.dest_name("dash_b", b))
        self.assertEqual(A.dest_name("dash_a", a), A.dest_name("dash_a", a))  # stable

    def test_svg_fallback(self):
        A = bl.Assets(bl.load(FEATURES), EXAMPLES)
        self.assertTrue(A.file_for("flow_svg").endswith(".svg"))
        self.assertTrue(A.file_for("flow_svg", raster_only=True).endswith(".png"))
        self.assertIsNone(A.file_for("flow_nofb", raster_only=True))
        self.assertTrue(any("flow_nofb" in w for w in A.warnings))


class SourcesAndSlides(unittest.TestCase):
    def test_numbering_and_footer(self):
        bp = bl.load(FEATURES)
        nums = bl.source_numbers(bp)
        self.assertEqual(nums["rfc8446"], 1)
        foot = bl.slide_footer(bp, next(s for s in bp["slides"] if s["id"] == "seq"))
        self.assertIn("RFC 8446", foot)
        self.assertIn("§2, Figure 1", foot)

    def test_credits_deduped_with_slides(self):
        bp = bl.load(FEATURES)
        entries = bl.source_entries(bp)
        credits = [e for e in entries if e["n"] is None]
        texts = [" ".join(e["parts"]) for e in credits]
        self.assertEqual(len([t for t in texts if "צילום מסך מקורי" in t]), 1)  # dash_a + dash_b merged

    def test_expand_targets(self):
        bp = bl.load(FEATURES)
        live = [s["id"] for s in bl.expand_slides(bp, "live")]
        pptx = [s["id"] for s in bl.expand_slides(bp, "pptx")]
        self.assertNotIn("quiz__answer", live)
        self.assertEqual(pptx[pptx.index("quiz") + 1], "quiz__answer")
        self.assertTrue(pptx[-1].startswith("_sources_"))

    def test_sources_split_across_slides(self):
        bp = load_json(FEATURES)
        bp["meta"]["sourcesPerSlide"] = 2
        out = bl.expand_slides(bl.normalise(bp), "live")
        self.assertEqual(sum(1 for s in out if s["id"].startswith("_sources_")), 2)


class SystemsAndCharts(unittest.TestCase):
    def test_presets_kept_and_aliases_resolve(self):
        for name in ("signal", "cobalt-grid", "swiss", "editorial", "mono"):
            self.assertEqual(bl.resolve_system({"system": name})[0], name)
        base, tok = bl.resolve_system({"system": "executive-data-briefing"})
        self.assertEqual(base, "signal")
        self.assertEqual(tok["frame"], "hairline")
        self.assertNotEqual(bl.resolve_system({"system": "keynote"})[1]["titleScale"],
                            bl.resolve_system({"system": "cobalt-grid"})[1]["titleScale"])

    def test_chart_spec(self):
        sp = bl.chart_spec({"kind": "line", "categories": ["a", "b"], "series": [{"name": "x", "values": [1.25, 2.5]}], "unit": "ms"})
        self.assertEqual(sp["decimals"], 2)
        self.assertEqual(bl.fmt_num(96.3, 1, "ms"), "96.3 ms")
        self.assertEqual(bl.fmt_num(38, 0, "%"), "38%")
        self.assertEqual(bl.excel_format(1, "ms"), '#,##0.0" ms"')
        self.assertEqual(bl.chart_spec({"kind": "pie"})["kind"], "unsupported")


class Merge(unittest.TestCase):
    def test_stage_ownership(self):
        base = bl.load(SAMPLE)
        designer = copy.deepcopy(base)
        designer["design"]["system"] = "swiss"
        designer["slides"][3]["layout"] = "full-exhibit"
        designer["slides"][3]["actionTitle"] = "designer must not change this"
        writer = copy.deepcopy(base)
        writer["slides"][3]["actionTitle"] = "Writer's sharper title"
        writer["slides"][3]["layout"] = "split"  # not the writer's field
        out = bl.merge(base, {"designer": designer, "writer": writer})
        self.assertEqual(out["design"]["system"], "swiss")
        self.assertEqual(out["slides"][3]["layout"], "full-exhibit")
        self.assertEqual(out["slides"][3]["actionTitle"], "Writer's sharper title")


if __name__ == "__main__":
    unittest.main()
