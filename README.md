# phishing-domain-monitor

Generates lookalike (typosquat) domain variants for a brand — omission,
duplication, transposition, keyboard substitution, hyphenation, TLD
swaps, and login-themed prefixes/suffixes — and scores each variant
by similarity to the real domain so the riskiest lookalikes surface
first. Day 2 checks the variants against a registered-domains list.

This is a **personal portfolio project** exploring typosquat detection
and security automation. It is a learning exercise, not a production
tool, and it has never been deployed at any employer.

## Quickstart

No dependencies to install — the standard library is all you need:

```bash
python3 run.py samples/brands.txt
python3 run.py samples/brands.txt --min-score 80
```

Exit codes: `2` = usage error or unreadable brands file, `0` = variants
generated (no findings model on day 1 — see day 2 for registered
variant alerts).

## Day-1 scope

- Variant generation: omission, duplication, transposition, keyboard
  substitution, hyphenation, vowel swaps, TLD swaps, login-themed
  affixes.
- Similarity scoring via edit distance, with a `--min-score` filter.
- Text and JSON (`--json`) output, highest score first.
