"""Moonlit Illusion Butterfly (달빛 환영 나비, title 달빛의 화신) mid-boss module generator, as a small package.

    python3 tools/build_mboss_butterfly.py

Layout (every file is plain Python, stdlib only):

    api.py       shared, stable: score names, damage coefficients, ranges, colours, the rig clip table (read
                 from tools/mboss_butterfly_rig_manifest.json, or the stub manifest while the real rig is not
                 merged), the Pattern record, the Gen writer helpers and the TL timeline that pattern modules use.
                 Pattern authors read it; they do not edit it.
    core.py      everything that is not a pattern: the 17 framework hooks, the form state machine (entrance,
                 human rotation, transformation, butterfly rotation, 달빛 해제, revert, groggy 300 t, turn and
                 chain re-form), the range-band shuffle bags, locomotion per form, the per-form hitbox, the wing
                 element looks, the Burning weakness, 달빛 고치 (debuff) and 달빛 축복 받음 (reward), the 달빛 이슬
                 heal orbs, entrance and death, HUD, test hooks and the generated pattern dispatchers.
    human.py     human-form patterns H1-H4 (달빛 발차기, 달빛 점프, 달빛 돌진, 광폭한 진공).
    wing.py      butterfly-form patterns B1-B4 (우아한 날개, 화염 날개의 습격, 날개 휩쓸개, 달빛 축복) and the
                 finale B5 달빛 해제 (service pattern 15; the core owns its form/groggy mechanics).
    stub_rig.py  + stub_rig_manifest.json: REMOVABLE stand-in rig (F:mboss/butterfly/rig_stub/) used only while
                 the real rig manifest does not exist.

A pattern module defines PATTERNS (a list of api.Pattern) and emit(gen). emit writes only
F:mboss/butterfly/p/<key>/** through gen.pw(key, name, lines): at least start, tick and cancel for every pattern it
declares, optionally vis (hz_vis events), pj_end (projectile events) and pause (the fight froze while it runs).
The full contract between the core and the pattern modules is the scratchpad file mb2/bf_contract.md.
"""

PATTERN_MODULES = ('human', 'wing')
