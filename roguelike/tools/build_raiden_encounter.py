"""Narukami encounter controller. Original Minecraft adaptation, no recorded audio.

    python3 tools/build_raiden_encounter.py

Generate controllers only; arena, hazards and articulated rig have separate builders.
The illusion challenge (pattern 5) lives in build_raiden_illusions.py; this file only
dispatches to illusion/tick and calls illusion/on_break and illusion/cleanup.

The generator is the package tools/raiden_enc/ (plan rd/plan.md E.0):
  core.py    helpers, balance constants, lifecycle, AI host (bag/choose/finish), damage in/out,
             objects, blink helpers, boss test commands
  lines.py   voice lines (typed subtitles) and caption state
  shogun.py  phase 0: patterns 1-7 and the eyes
  tenma.py   transformation, phase 2 patterns 11-18, exhausted, armour shield
The phase modules hand their bag, close-in reach and tick/choose hooks to core as data.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import raiden_enc  # noqa: E402

raiden_enc.build()
print('Generated Narukami encounter controllers, 13 attack timelines + illusion hook, and boss test commands.')
