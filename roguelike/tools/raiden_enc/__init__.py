"""Raiden (마가츠 미타케 나루카미노 미코토) encounter generator package (plan rd/plan.md E.0).

core    helpers, balance constants, lifecycle, AI host (bag / choose / finish), damage in/out, objects, tests (S2-SHOGUN)
lines   voice lines and caption state (S2-SHOGUN)
shogun  phase 0: patterns 1-7, eyes (S2-SHOGUN)
tenma   transformation, phase 2 patterns 11-18, exhausted, shield (S2-TENMA)
"""
from . import core, lines, shogun, tenma


def build():
    # M1 seam (rd/s2_notes.md §3): tenma.VOICE_LINES adds keys to lines.LINES or replaces a Tenma-owned entry in place
    # (the id order of lines.LINES is kept, so the generated line ids only change for new keys).
    lines.LINES.update(tenma.VOICE_LINES)
    lines.LINE_IDS.clear()
    lines.LINE_IDS.update({k: i for i, k in enumerate(lines.LINES, 1)})
    lines.build()
    core.build(shogun, tenma)
    shogun.build()
    tenma.build()
    core.write_patterns()
