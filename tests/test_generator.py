#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generator import find_chromium, SAMPLE_DECK_HTML

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

if __name__ == "__main__":
    unittest.main()
