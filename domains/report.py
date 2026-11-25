"""Render scored variants as text or JSON."""

import json


def render_text(brand, scored):
    """Render scored variants, highest score first."""
    lines = [f"brand: {brand} — {len(scored)} variant(s)"]
    for variant, technique, points in scored:
        lines.append(f"{points:3d} [{technique}] {variant}")
    return "\n".join(lines)


def render_json(brand, scored):
    """Render scored variants as JSON."""
    return json.dumps({
        "brand": brand,
        "variants": [
            {"domain": v, "technique": t, "score": s}
            for v, t, s in scored
        ],
    }, indent=2)
