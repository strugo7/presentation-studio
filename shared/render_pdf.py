# -*- coding: utf-8 -*-
"""blueprint.json -> deck.pdf   (static, fonts embedded)

Two routes (both produce a 16:9 page-per-slide PDF; pick with --from):
  --from=html  (default)  blueprint -> HTML print build -> headless Chrome --print-to-pdf
  --from=pptx             blueprint -> PPTX -> pptx_to_html -> headless Chrome --print-to-pdf

Needs Google Chrome (or Chromium). If LibreOffice `soffice` is on PATH it is used for the pptx route
instead (higher fidelity); otherwise Chrome.

Usage:  python render_pdf.py blueprint.json out.pdf [assets_dir] [--from=html|pptx] [--font=path.ttf]
"""
import sys, os, subprocess, tempfile, shutil, time, glob

args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = {a.split("=", 1)[0][2:]: (a.split("=", 1)[1] if "=" in a else True) for a in sys.argv[1:] if a.startswith("--")}
BP, OUT = args[0], args[1]
ASSETS = args[2] if len(args) > 2 else os.path.dirname(os.path.abspath(BP))
FROM = flags.get("from", "html")
FONT = flags.get("font")
HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

def chrome():
    for c in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              shutil.which("google-chrome"), shutil.which("chromium")]:
        if c and os.path.exists(c): return c
    raise SystemExit("Chrome/Chromium not found — install it, or use the pptx route with LibreOffice.")

def chrome_print(index_html, out_pdf):
    prof = tempfile.mkdtemp(prefix="pschrome_")
    p = subprocess.Popen([chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                          "--run-all-compositor-stages-before-draw", "--virtual-time-budget=15000",
                          "--user-data-dir=" + prof, "--print-to-pdf=" + out_pdf, "file://" + os.path.abspath(index_html)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(90):
        if os.path.exists(out_pdf) and os.path.getsize(out_pdf) > 0: break
        time.sleep(1)
    time.sleep(2); p.kill(); shutil.rmtree(prof, ignore_errors=True)
    if not (os.path.exists(out_pdf) and os.path.getsize(out_pdf) > 0): raise SystemExit("Chrome did not produce a PDF.")

tmp = tempfile.mkdtemp(prefix="pspdf_")
try:
    if FROM == "pptx":
        pptx = os.path.join(tmp, "deck.pptx")
        subprocess.check_call([PY, os.path.join(HERE, "render_pptx.py"), BP, pptx, ASSETS])
        soffice = shutil.which("soffice")
        if soffice:
            subprocess.check_call([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, pptx])
            shutil.move(glob.glob(os.path.join(tmp, "*.pdf"))[0], OUT)
        else:
            hdir = os.path.join(tmp, "h")
            subprocess.check_call([PY, os.path.join(HERE, "pptx_to_html.py"), pptx, hdir])
            chrome_print(os.path.join(hdir, "index.html"), OUT)
    else:
        hdir = os.path.join(tmp, "h")
        cmd = [PY, os.path.join(HERE, "render_html.py"), BP, hdir, ASSETS, "--pdf"]
        if FONT: cmd.append("--font=" + FONT)
        subprocess.check_call(cmd)
        chrome_print(os.path.join(hdir, "index.html"), OUT)
    print("saved", OUT, "(%.1f MB)" % (os.path.getsize(OUT) / 1e6), "| route:", FROM)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
