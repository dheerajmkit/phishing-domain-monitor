# Usage

## Generating variants

```bash
python3 run.py brands.txt
python3 run.py brands.txt --min-score 80   # only close lookalikes
python3 run.py brands.txt --json           # machine-readable output
```

The brands file holds one domain per line. Variants are scored 0–100
by edit-distance similarity; TLD swaps keep a floor of 80 and
login-themed affixes a floor of 70, because they are deceptive even
when the edit distance is larger.

## Checking registered domains

```bash
python3 run.py brands.txt --registered registered.txt
```

Variants that appear in the registered-domains list are reported as
findings: HIGH at score 85+, MEDIUM below. Exit code `1` means at
least one HIGH registered lookalike; `0` means none; `2` means a file
could not be read.

## Variant techniques

Omission, duplication, transposition, keyboard substitution,
hyphenation, vowel swaps, TLD swaps (`com`/`net`/`org`/`co`/`io`/
`app`), and login-themed affixes (`login`, `secure`, `verify`,
`account`, `support`, `help`).

## Running the tests

```bash
python3 -m unittest discover -s tests -v
```
