#!/bin/sh
# Generate variants and check the registered list, then run tests.
set -e
cd "$(dirname "$0")/.."
python3 run.py samples/brands.txt --registered samples/registered.txt || true
python3 -m unittest discover -s tests -v
