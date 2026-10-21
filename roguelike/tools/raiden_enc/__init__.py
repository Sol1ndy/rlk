"""Raiden (마가츠 미타케 나루카미노 미코토) encounter generator package (plan rd/plan.md E.0).

core    helpers, balance constants, lifecycle, AI host (bag / choose / finish), damage in/out, objects, tests (S2-SHOGUN)
lines   voice lines and caption state (S2-SHOGUN)
shogun  phase 0: patterns 1-7, eyes (S2-SHOGUN)
tenma   transformation, phase 2 patterns 11-18, exhausted, shield (S2-TENMA)
"""
from . import core, lines, shogun, tenma


def build():
    lines.build()
    core.build(shogun, tenma)
    shogun.build()
    tenma.build()
    core.write_patterns()
