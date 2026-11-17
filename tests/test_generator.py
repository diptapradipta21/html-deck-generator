#!/usr/bin/env python3
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generator import find_chromium, main, render_html_to_pdf, SAMPLE_DECK_HTML

class TestDeckGenerator(unittest.TestCase):
    def test_sample_deck_html_structure(self):
        self.assertIn("<!DOCTYPE html>", SAMPLE_DECK_HTML)
        self.assertIn(".slide", SAMPLE_DECK_HTML)
        self.assertIn("Executive Strategic Deck", SAMPLE_DECK_HTML)
        self.assertIn("1920px 1080px", SAMPLE_DECK_HTML)

    def test_find_chromium_returns_path_or_command(self):
        binary = find_chromium()
        self.assertIsInstance(binary, str)
        self.assertTrue(len(binary) > 0)

    @patch("shutil.which")
    @patch("glob.glob")
    def test_find_chromium_fallback_path(self, mock_glob, mock_which):
        mock_glob.return_value = []
        mock_which.return_value = None
        # Should fallback to candidates or 'chrome'
        result = find_chromium()
        self.assertIsInstance(result, str)

    def test_scaffold_output_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "deck.html"
            target.write_text(SAMPLE_DECK_HTML, encoding="utf-8")
            self.assertTrue(target.exists())
            self.assertGreater(target.stat().st_size, 500)

    @patch("subprocess.run")
    def test_render_timeout_returns_false(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="chrome", timeout=1)
        with tempfile.TemporaryDirectory() as tmpdir:
            html = Path(tmpdir) / "deck.html"
            html.write_text(SAMPLE_DECK_HTML, encoding="utf-8")
            ok = render_html_to_pdf(str(html), str(Path(tmpdir) / "out.pdf"), timeout=1)
            self.assertFalse(ok)

    def test_scaffold_refuses_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "deck.html"
            target.write_text("existing deck", encoding="utf-8")
            with patch.object(sys, "argv", ["generator.py", "--scaffold", str(target)]):
                with self.assertRaises(SystemExit) as ctx:
                    main()
            self.assertEqual(ctx.exception.code, 1)
            self.assertEqual(target.read_text(encoding="utf-8"), "existing deck")

    def test_scaffold_overwrites_with_force(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "deck.html"
            target.write_text("existing deck", encoding="utf-8")
            with patch.object(sys, "argv", ["generator.py", "--scaffold", str(target), "--force"]):
                with self.assertRaises(SystemExit) as ctx:
                    main()
            self.assertEqual(ctx.exception.code, 0)
            self.assertIn("<!DOCTYPE html>", target.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
