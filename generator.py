#!/usr/bin/env python3
"""
html-deck-generator — 16:9 Widescreen Apple Keynote / Linear Tier HTML Presentation to PDF CLI.
Converts clean, responsive HTML slide decks into pixel-perfect executive PDF presentations
using Headless Chromium with zero text clipping and high-contrast dark themes.
"""

import os
import sys
import glob
import argparse
import subprocess
import shutil
from pathlib import Path

DEFAULT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap');

@page {
  size: 1920px 1080px;
  margin: 0;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}

body {
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  background-color: #060911;
  color: #F8FAFC;
}

.slide {
  width: 1920px;
  height: 1080px;
  page-break-after: always;
  page-break-inside: avoid;
  position: relative;
  overflow: hidden;
  padding: 60px 80px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: radial-gradient(circle at 85% 15%, rgba(30, 58, 138, 0.25) 0%, #060911 70%);
}

.title-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 9999px;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.4);
  color: #60A5FA;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 20px;
}

h1 {
  font-size: 56px;
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: #FFFFFF;
}

p.subtitle {
  font-size: 24px;
  color: #94A3B8;
  margin-top: 16px;
  max-width: 900px;
  line-height: 1.4;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  margin-top: 40px;
}

.card {
  background: rgba(15, 23, 42, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 32px;
}

.card h3 {
  font-size: 22px;
  font-weight: 700;
  color: #F1F5F9;
  margin-bottom: 12px;
}

.card p {
  font-size: 16px;
  color: #94A3B8;
  line-height: 1.5;
}

.metric {
  font-size: 48px;
  font-weight: 900;
  color: #38BDF8;
  margin-bottom: 8px;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #475569;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 20px;
}
"""

SAMPLE_DECK_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Executive Strategic Deck</title>
  <style>
{DEFAULT_CSS}
  </style>
</head>
<body>
  <!-- Slide 1: Cover -->
  <section class="slide">
    <div>
      <span class="title-badge">Strategic Roadmap</span>
      <h1>Autonomous AI Agent Ecosystem<br><span style="color: #38BDF8;">Executive Briefing</span></h1>
      <p class="subtitle">Next-generation orchestration, self-healing cron daemons, and zero-token intelligence.</p>
    </div>
    <div class="footer">
      <span>Executive Steering Committee</span>
      <span>Confidential • 2026</span>
    </div>
  </section>

  <!-- Slide 2: Metrics -->
  <section class="slide">
    <div>
      <span class="title-badge">Operational Performance</span>
      <h1>Key Growth Indicators</h1>
      <div class="grid-3">
        <div class="card">
          <div class="metric">12+</div>
          <h3>Active Repositories</h3>
          <p>Autonomous maintenance with daily compiler checks and continuous refactoring.</p>
        </div>
        <div class="card">
          <div class="metric">0 Token</div>
          <h3>Local RAG Search</h3>
          <p>Instant BM25 ranking across knowledge notes without cloud vector DB overhead.</p>
        </div>
        <div class="card">
          <div class="metric">99.9%</div>
          <h3>Telegram Delivery</h3>
          <p>Reliable division thread routing through dedicated Bot API forum topics.</p>
        </div>
      </div>
    </div>
    <div class="footer">
      <span>Page 2 / 2</span>
      <span>Autonomous Agent Engine</span>
    </div>
  </section>
</body>
</html>
"""

def find_chromium():
    # Dynamic search in Playwright cache
    pw_matches = glob.glob("/opt/data/home/.cache/ms-playwright/chromium-*/chrome-linux64/chrome")
    if pw_matches:
        return sorted(pw_matches)[-1]

    # Dynamic search in system PATH
    for bin_name in ["chromium-browser", "google-chrome", "chromium", "google-chrome-stable", "chrome"]:
        found = shutil.which(bin_name)
        if found:
            return found

    candidates = [
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return "chrome"

def render_html_to_pdf(input_html: str, output_pdf: str, chrome_path: str = None):
    chrome = chrome_path or find_chromium()
    in_path = Path(input_html).resolve()
    out_path = Path(output_pdf).resolve()

    print(f"[*] Rendering {in_path.name} to {out_path.name} via Chromium...")
    cmd = [
        chrome,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out_path}",
        str(in_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if out_path.exists() and out_path.stat().st_size > 0:
        print(f"[✓] Rendered PDF successfully! ({out_path.stat().st_size / 1024:.1f} KB)")
        return True
    else:
        print(f"[-] Chromium render failed: {res.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Apple Keynote / Linear Tier HTML-to-PDF Slide Deck Compiler.")
    parser.add_argument("input", nargs="?", help="Path to input HTML slide deck")
    parser.add_argument("--output", "-o", default="output.pdf", help="Destination PDF file path (default: output.pdf)")
    parser.add_argument("--chrome", help="Custom Chromium / Chrome executable binary path")
    parser.add_argument("--scaffold", metavar="FILENAME", help="Scaffold a new executive HTML slide deck boilerplate")
    parser.add_argument("--check-chrome", action="store_true", help="Probe and display detected Chromium/Chrome binary path")

    args = parser.parse_args()

    if args.check_chrome:
        binary = find_chromium()
        exists = Path(binary).exists() if binary else False
        status_symbol = "[✓]" if exists else "[!]"
        print(f"{status_symbol} Detected Chromium binary: {binary} (available: {exists})")
        sys.exit(0 if exists else 1)

    if args.scaffold:
        out_file = Path(args.scaffold)
        out_file.write_text(SAMPLE_DECK_HTML, encoding="utf-8")
        print(f"[✓] Scaffolded executive HTML presentation template to: {out_file.resolve()}")
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(1)

    success = render_html_to_pdf(args.input, args.output, args.chrome)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
