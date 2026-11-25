"""Similarity scoring for lookalike domains."""


def levenshtein(a, b):
    """Edit distance between two strings (dynamic programming)."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def score(variant, original, technique):
    """Score a variant 0-100; higher means a closer lookalike.

    Edit distance drives the score; TLD swaps and affixes are
    intrinsically deceptive, so they keep a high floor.
    """
    distance = levenshtein(variant, original)
    longest = max(len(variant), len(original))
    similarity = 1 - distance / longest if longest else 0
    base = round(100 * similarity)
    if technique == "tld-swap":
        return max(base, 80)
    if technique == "affix":
        return max(base, 70)
    return base
