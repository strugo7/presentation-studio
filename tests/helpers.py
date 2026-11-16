# -*- coding: utf-8 -*-
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = os.path.join(ROOT, "shared")
EXAMPLES = os.path.join(ROOT, "examples")
SAMPLE = os.path.join(EXAMPLES, "sample-blueprint.json")
FEATURES = os.path.join(EXAMPLES, "features-blueprint.json")
sys.path.insert(0, SHARED)
import blueprint_lib as bl  # noqa: E402,F401


def run_script(name, *args, timeout=240):
    p = subprocess.run([sys.executable, os.path.join(SHARED, name)] + list(args),
                       capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise AssertionError("%s failed (%d):\n%s\n%s" % (name, p.returncode, p.stdout, p.stderr))
    return p.stdout


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_tmp_blueprint(bp, tmpdir, name="bp.json"):
    path = os.path.join(tmpdir, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bp, f, ensure_ascii=False)
    return path


def chrome_available():
    return any(shutil.which(c) for c in ("google-chrome", "chromium", "chromium-browser")) or \
        os.path.exists("/Applications/Google Chrome.app")


def node_playwright_available():
    if not shutil.which("node"):
        return False
    p = subprocess.run(["node", "-e", "require('playwright')"], capture_output=True)
    return p.returncode == 0


class TmpDirMixin:
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="pstest_")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
