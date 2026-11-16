# -*- coding: utf-8 -*-
"""Validate a blueprint: JSON schema + cross-references (sources, assets, sections, quiz answers).

Usage:  python shared/validate_blueprint.py blueprint.json [assets_dir] [--strict]
Exit 1 on errors (or on warnings with --strict). Run it at every hand-off between stages.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blueprint_lib as bl  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    raise SystemExit(__doc__)
path = args[0]
assets_dir = args[1] if len(args) > 1 else os.path.dirname(os.path.abspath(path))
bp = bl.load(path)
errors, warnings = bl.validate(bp, assets_dir)
for e in errors:
    print("ERROR   ", e)
for w in warnings:
    print("warning ", w)
print("%s: %d error(s), %d warning(s)" % (path, len(errors), len(warnings)))
sys.exit(1 if errors or ("--strict" in sys.argv and warnings) else 0)
