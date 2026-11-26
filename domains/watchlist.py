"""Check generated variants against a registered-domains list.

A variant that is actually registered is a live lookalike risk: it
can already host a phishing page. Severity follows the similarity
score.
"""

from .typosquat import variants
from .scoring import score


def load_registered(path):
    """Load a registered-domains file (one domain per line)."""
    with open(path, encoding="utf-8") as fh:
        return {line.strip().lower() for line in fh if line.strip()}


def check_registered(brand, registered, min_score=70):
    """Return findings for variants present in the registered set."""
    findings = []
    for variant, technique in variants(brand):
        if variant not in registered:
            continue
        points = score(variant, brand, technique)
        if points < min_score:
            continue
        findings.append({
            "check": "variant-registered",
            "severity": "HIGH" if points >= 85 else "MEDIUM",
            "object": variant,
            "message": f"lookalike {variant} of {brand} is registered "
                       f"(score {points}, {technique})",
        })
    return sorted(findings, key=lambda f: f["object"])
