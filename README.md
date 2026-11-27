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
python3 run.py samples/brands.txt --registered samples/registered.txt
```

Exit codes: `2` = usage error or unreadable brands file, `1` = at
least one HIGH registered lookalike (with `--registered`), `0` =
no HIGH findings.

## Day-3 scope

- Unit tests (`tests/test_checks.py`): run with
  `python3 -m unittest discover -s tests -v`.
- Full usage guide (`docs/USAGE.md`) and a demo script
  (`examples/run-all.sh`).

## Day-2 scope

- Registered-variant alerts (`--registered`): variants that appear
  in a registered-domains list are reported as findings — HIGH at
  score 85+, MEDIUM below — with exit code `1` when any HIGH
  lookalike is registered.

## Day-1 scope

## Day-1 scope

- Variant generation: omission, duplication, transposition, keyboard
  substitution, hyphenation, vowel swaps, TLD swaps, login-themed
  affixes.
- Similarity scoring via edit distance, with a `--min-score` filter.
- Text and JSON (`--json`) output, highest score first.
