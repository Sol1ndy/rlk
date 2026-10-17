"""Corrupted Guardian (파수꾼・타락) mid-boss module generator, as a small package.

    python3 tools/build_mboss_guardian.py

Layout (every file is plain Python, stdlib only):

    api.py   shared, stable: score names, damage coefficients, ranges, colours, the rig clip table
             (read from tools/mboss_guardian_rig_manifest.json), the Pattern record and the Gen
             writer helpers that pattern modules call. Pattern authors read it; they do not edit it.
    core.py  everything that is not a pattern: the 16 framework hooks, the AI state machine and the
             rotation (shuffle bag, range bands, close-in), guard mode and the element record,
             chaos (flight, charge, timer, stars, cube streams, haze), groggy, entrance, death,
             voice lines, HUD, test hooks, and the generated pattern dispatchers.
    p12.py   P1 공간 찌르기 (two thrusts), P2 공간 투창 (javelin).
    p34.py   P3 공간을 집행하는 시련 (melee slam), P4 어둠 속에서 퍼지는 공간 (pull + two 360 swings).
    p56.py   P5 하늘을 심판하는 자 (fly-slam), P6 guard sweeps (gold / enchanted, with the
             element-coloured strike fx) and the chaos fail spears.

A pattern module defines PATTERNS (a list of api.Pattern) and emit(gen). emit writes only
F:mboss/guardian/p/<key>/** through gen.pw(key, name, lines): at least start, tick and cancel
for every pattern it declares, optionally vis (hz_vis events) and pj_end (projectile events).
The full contract between the core and the pattern modules is in the scratchpad file
mboss/gd_contract.md and in the header comments of the generated F:mboss/guardian/p/* files.
"""

PATTERN_MODULES = ('p12', 'p34', 'p56')
