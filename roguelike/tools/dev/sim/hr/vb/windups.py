#!/usr/bin/env python3
"""windups.py — per hit of the fight the swing and the wind-up of its clip, from the blade track (round V, lane VB).

    python3 -I windups.py <roguelike> [--track <blade_track.json of an --only build>]

Prints, per hit: the swing [a, b], the tick w from which the wind-up pose is held, the lead h - w and the rule (10 for a single /
first hit, 6 for a chain follow-up; a gauntlet cut: the pose before its clip counts, see test_blade.py). Exit 1 if a rule fails.
"""
import json
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(WT / 'tools'))
sys.dont_write_bytecode = True
from mboss_scarlet import api, blade  # noqa: E402

if '--track' in sys.argv:
    blade._TRACK.update(json.loads(Path(sys.argv[sys.argv.index('--track') + 1]).read_text())['clips'])
bad = 0
for key, rows in api.HITS.items():
    prev, seen = None, set()
    for row in rows:
        clip, ev = row[0], row[1]
        if (clip, ev) in seen or clip not in blade._TRACK and '--track' in sys.argv:
            continue
        seen.add((clip, ev))
        if key in ('a3s',):
            continue
        sw = blade.swing_of(clip, ev)
        first = prev is None or prev[0] != clip or sw.h - prev[1] > 24
        need = blade.LEAD_FIRST if first else blade.LEAD_CHAIN
        lead = sw.h - sw.w
        ok = lead >= need
        bad += not ok
        print(f'{"ok  " if ok else "FAIL"} {key:6s} {clip:7s} {ev:6s} h {sw.h:3d} swing {sw.a:3d}-{sw.b:3d} wound from {sw.w:3d} lead {lead:2d} (rule {need})')
        prev = (clip, sw.h)
sys.exit(1 if bad else 0)
