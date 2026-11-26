#!/usr/bin/env python3
"""Generate and score lookalike (typosquat) domains for brands.

Usage:
    python3 run.py <brands.txt> [--min-score N] [--json]

The brands file holds one domain per line. Exit codes: 2 = usage
error / unreadable file, 0 = variants generated.
"""

import argparse
import sys

from domains.typosquat import variants
from domains.scoring import score
from domains.watchlist import load_registered, check_registered
from domains.report import render_text, render_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brands", help="file with one domain per line")
    parser.add_argument("--min-score", type=int, default=70,
                        help="only show variants scoring at least N")
    parser.add_argument("--json", action="store_true",
                        help="emit variants as JSON")
    parser.add_argument("--registered",
                        help="registered-domains file to check variants against")
    args = parser.parse_args(argv)

    try:
        with open(args.brands, encoding="utf-8") as fh:
            brands = [line.strip() for line in fh if line.strip()]
    except OSError as exc:
        print(f"error: cannot read brands file: {exc}", file=sys.stderr)
        return 2

    registered = None
    if args.registered:
        try:
            registered = load_registered(args.registered)
        except OSError as exc:
            print(f"error: cannot read registered file: {exc}",
                  file=sys.stderr)
            return 2

    exit_code = 0
    for brand in brands:
        if registered is not None:
            findings = check_registered(brand, registered, args.min_score)
            if args.json:
                import json
                print(json.dumps({"brand": brand, "findings": findings},
                                 indent=2))
            else:
                print(f"brand: {brand} — {len(findings)} registered "
                      "lookalike(s)")
                for f in findings:
                    print(f"[{f['severity']}] {f['check']} "
                          f"({f['object']}): {f['message']}")
            if any(f["severity"] == "HIGH" for f in findings):
                exit_code = 1
            continue
        scored = sorted(
            ((v, t, score(v, brand, t)) for v, t in variants(brand)),
            key=lambda item: (-item[2], item[0]))
        scored = [item for item in scored if item[2] >= args.min_score]
        if args.json:
            print(render_json(brand, scored))
        else:
            print(render_text(brand, scored))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
