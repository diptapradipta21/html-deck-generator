# 📊 HTML Deck Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![16:9 Widescreen](https://img.shields.io/badge/Format-16%3A9%20Executive-purple.svg)](#)
[![Zero Clipping](https://img.shields.io/badge/Clipping-Zero%20Breakage-brightgreen.svg)](#)

> **CLI compiler and master layout boilerplate to render 16:9 widescreen HTML slide decks into pixel-perfect executive PDF presentations via Headless Chromium.**

---

## 💡 The Problem
Tools like Marp, Reveal.js, and Slidev frequently break when compiling AI-generated presentations: fonts get clipped, card borders overflow viewports, and background gradients are stripped by print drivers.

## 🚀 The Solution
`html-deck-generator` enforces strict `@page { size: 1920px 1080px }` viewport anchoring, WebKit print-color enforcement, and compositor flags to deliver pristine boardroom-grade PDFs every single time.

---

## ⚡ Quick Start

```bash
# 1. Scaffold a fresh executive presentation deck
python3 generator.py --scaffold presentation.html

# 2. Compile HTML slides to pixel-perfect 16:9 PDF
python3 generator.py presentation.html -o Boardroom_Deck.pdf
```

---

## 🛠️ Features
- **Dynamic Chromium Discovery:** Auto-detects Playwright cache, headless Linux Chromium, and Google Chrome binaries.
- **Instant Scaffolding:** `--scaffold` generates a ready-to-present executive deck with typography, cards, and dark gradients.
- **Zero-Clipping Compositor:** Uses `--headless=new` and `--run-all-compositor-stages-before-draw` to prevent partial font renders.

---

## 📄 License
MIT License - Copyright (c) 2026 Fajar Indra Pradipta Gajah.
