"""Lookalike (typosquat) domain variant generation."""

KEYBOARD_NEIGHBORS = {
    "a": "qwsz", "b": "vghn", "c": "xdfv", "d": "serfcx", "e": "wsdr",
    "f": "drtgvc", "g": "ftyhbv", "h": "gyujnb", "i": "ujko",
    "j": "huikmn", "k": "jiolm", "l": "kop", "m": "njk",
    "n": "bjhm", "o": "iklp", "p": "ol", "q": "wa",
    "r": "edft", "s": "awedxz", "t": "rfgy", "u": "yhji",
    "v": "cfgb", "w": "qase", "x": "zsdc", "y": "tghu", "z": "asx",
}

TLD_SWAPS = ("com", "net", "org", "co", "io", "app")
AFFIXES = ("login", "secure", "verify", "account", "support", "help")
VOWELS = "aeiou"


def _split(domain):
    domain = domain.strip().lower().rstrip(".")
    if "." not in domain:
        return domain, ""
    label, tld = domain.rsplit(".", 1)
    return label, tld


def _omissions(label):
    return {label[:i] + label[i + 1:] for i in range(len(label))}


def _duplications(label):
    return {label[:i] + label[i] + label[i:]
            for i in range(len(label))}


def _transpositions(label):
    return {label[:i] + label[i + 1] + label[i] + label[i + 2:]
            for i in range(len(label) - 1)}


def _substitutions(label):
    out = set()
    for i, ch in enumerate(label):
        for repl in KEYBOARD_NEIGHBORS.get(ch, ""):
            out.add(label[:i] + repl + label[i + 1:])
    return out


def _hyphenations(label):
    return {label[:i] + "-" + label[i:] for i in range(1, len(label))}


def _vowel_swaps(label):
    out = set()
    for i, ch in enumerate(label):
        if ch in VOWELS:
            for repl in VOWELS:
                if repl != ch:
                    out.add(label[:i] + repl + label[i + 1:])
    return out


def _label_variants(label):
    out = set()
    out |= _omissions(label)
    out |= _duplications(label)
    out |= _transpositions(label)
    out |= _substitutions(label)
    out |= _hyphenations(label)
    out |= _vowel_swaps(label)
    out.discard(label)
    out.discard("")
    return out


def variants(domain):
    """Return {(variant_domain, technique)} for one brand domain."""
    label, tld = _split(domain)
    found = set()
    for variant in _label_variants(label):
        found.add((f"{variant}.{tld}", "label"))
    for swap in TLD_SWAPS:
        if swap != tld:
            found.add((f"{label}.{swap}", "tld-swap"))
    for affix in AFFIXES:
        found.add((f"{affix}-{label}.{tld}", "affix"))
        found.add((f"{label}-{affix}.{tld}", "affix"))
    found.discard((domain.strip().lower(), "label"))
    return found
