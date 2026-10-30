#!/usr/bin/env python3
"""
html-deck-generator — 16:9 Widescreen Apple Keynote / Linear Tier HTML Presentation to PDF CLI.
Converts clean, responsive HTML slide decks into pixel-perfect executive PDF presentations
using Headless Chromium with zero text clipping and high-contrast dark themes.
"""

import os
import sys
import argparse
import subprocess
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
  padding: 50px 70px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: radial-gradient(circle at 80% 20%, rgba(30, 58, 138, 0.22) 0%, #060911 70%);
}
"""

def find_chromium():
    candidates = [
        "/opt/data/home/.cache/ms-playwright/chromium-1247/chrome-linux64/chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
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
    parser.add_argument("input", help="Path to input HTML slide deck")
    parser.add_argument("--output", "-o", default="output.pdf", help="Destination PDF file path (default: output.pdf)")
    parser.add_argument("--chrome", help="Custom Chromium / Chrome executable binary path")

    args = parser.parse_args()
    success = render_html_to_pdf(args.input, args.output, args.chrome)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
