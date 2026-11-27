"""Unit tests for typosquat generation, scoring, and watchlist checks.

Run from the project root:  python3 -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domains.typosquat import variants
from domains.scoring import levenshtein, score
from domains.watchlist import check_registered


class TestVariants(unittest.TestCase):
    def test_omission_present(self):
        names = {v for v, _ in variants("acme.com")}
        self.assertIn("ace.com", names)
        self.assertIn("acm.com", names)

    def test_transposition_present(self):
        names = {v for v, _ in variants("acme.com")}
        self.assertIn("amce.com", names)

    def test_tld_swap_present(self):
        names = {v for v, _ in variants("acme.com")}
        self.assertIn("acme.net", names)
        self.assertIn("acme.co", names)

    def test_affix_present(self):
        names = {v for v, _ in variants("acme.com")}
        self.assertIn("login-acme.com", names)
        self.assertIn("acme-secure.com", names)

    def test_original_excluded(self):
        names = {v for v, _ in variants("acme.com")}
        self.assertNotIn("acme.com", names)


class TestScoring(unittest.TestCase):
    def test_levenshtein(self):
        self.assertEqual(levenshtein("acme", "acme"), 0)
        self.assertEqual(levenshtein("acme", "acm"), 1)
        self.assertEqual(levenshtein("kitten", "sitting"), 3)

    def test_close_variant_scores_high(self):
        self.assertGreaterEqual(score("acmme.com", "acme.com", "label"), 85)

    def test_tld_swap_floor(self):
        self.assertGreaterEqual(score("acme.co", "acme.com", "tld-swap"), 80)


class TestWatchlist(unittest.TestCase):
    def test_registered_variant_flagged(self):
        findings = check_registered("acme.com", {"acme.co", "other.org"})
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["object"], "acme.co")
        self.assertEqual(findings[0]["severity"], "HIGH")

    def test_unregistered_is_clean(self):
        findings = check_registered("acme.com", {"other.org"})
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
