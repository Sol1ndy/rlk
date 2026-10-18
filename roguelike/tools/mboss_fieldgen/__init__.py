"""Field generator (실험성 역장 발생 장치, nameplate 브레게 프로토타입) mid-boss module generator, as a small package.

    python3 tools/build_mboss_fieldgen.py

Layout (every file is plain Python, stdlib only; copied from tools/mboss_butterfly/ and renamed):

    api.py       shared, stable: score names, damage coefficients, ranges, colours, the HUD glyph table (font
                 rlk:mboss_fg of the fx kit), the rig clip table (read from tools/mboss_fieldgen_rig_manifest.json, or
                 the stub manifest while the real rig is not merged), the Pattern record, the Gen writer helpers, the TL
                 timeline and the shared 파쇄 helper (rocks) that pattern modules use, and the fx kit's call builders
                 (api.K; Gen.fx, snd, kcard, kprop, klook, khud, tele_*). Pattern authors read it; they do not edit it.
    core.py      everything that is not a pattern: the 17 framework hooks, the state machine (entrance, the cruise
                 rotation with its range-band bag, the field trigger, the field sequence: warp, 「인력 충격파」 x3, field
                 patterns, closing waves, pack-up), the 20-hit break meter (counting rules, HUD, crack stages), the
                 break, groggy 200 t and recovery, the field damage cut, low gravity on / off, the body clamp r 16.5,
                 the per-form hitbox, death, pause, reload, uninstall, tests, the fx kit wiring (hooks, the meter
                 protocol, the banner, the boss-bar lines), the core's remaining vanilla fx (cfx/) and the generated
                 pattern dispatchers.
    cruise.py    cruise patterns C1-C6 (일점 상쇄, 내려찍기, 코어, 바위 폭탄, 지면 충격, 파쇄).
    field.py     field patterns F1-F2 (감소 영역, 파쇄) and the service pattern 21 「인력 충격파」 x3.
    stub_rig.py  + stub_rig_manifest.json: REMOVABLE stand-in rig (F:mboss/fieldgen/rig_stub/) used only while the
                 real rig manifest does not exist.

A pattern module defines PATTERNS (a list of api.Pattern) and emit(gen). emit writes only F:mboss/fieldgen/p/<key>/**
through gen.pw(key, name, lines): at least start, tick and cancel for every pattern it declares, optionally vis
(hz_vis events), pj_end (projectile events) and pause (the fight froze while it runs). The full contract between the
core and the pattern modules is the scratchpad file mb3/fg_contract.md.
"""

PATTERN_MODULES = ('cruise', 'field')
