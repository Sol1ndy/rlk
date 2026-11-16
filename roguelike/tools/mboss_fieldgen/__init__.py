"""Field generator (실험성 역장 발생 장치, nameplate 브레게 프로토타입) mid-boss module generator, as a small package.

    python3 tools/build_mboss_fieldgen.py

Layout (every file is plain Python, stdlib only; copied from tools/mboss_butterfly/ and renamed):

    api.py       shared, stable: score names, damage coefficients, ranges, colours, the HUD glyph table (font
                 rlk:mboss_fg of the fx kit), the rig clip table (read from tools/mboss_fieldgen_rig_manifest.json, the
                 rig generator's; required), the Pattern record, the Gen writer helpers, the TL
                 timeline and the shared 파쇄 helper (c_rocks) that pattern modules use, and the fx kit's call builders
                 (api.K; Gen.fx, snd, kcard, kprop, klook, khud, tele_*). Pattern authors read it; they do not edit it.
                 Telegraph rule (10-20, user): a ground decal only where the reference footage shows one (C5, F1, the
                 C1 / C2 slam's base flare); every other attack is read from the boss's motion and sound.
    core.py      everything that is not a pattern: the 17 framework hooks, the state machine (entrance, the cruise
                 rotation with its range-band bag, the field trigger, the field sequence: warp, 「인력 충격파」 x3, field
                 patterns, closing waves, pack-up), the 20-hit break meter (counting rules, HUD, crack stages), the
                 break, groggy 200 t and recovery, the field damage cut, low gravity on / off, the body clamp r 16.5,
                 the per-form hitbox, death, pause, reload, uninstall, tests, the fx kit wiring (hooks, the meter
                 protocol, the banner, the boss-bar lines) and the generated pattern dispatchers.
    cruise.py    cruise patterns C1-C6 (일점 상쇄, 내려찍기, 코어, 바위 폭탄, 지면 충격, 파쇄).
    seq_c.py     the entrance (E) and death (S4) sequences (F:mboss/fieldgen/seq_c/**), called by the core's hooks.
    field.py     field patterns F1-F2 (감소 영역, 파쇄) and the service pattern 21 「인력 충격파」 x3.
    seq_f.py     the field sequences: the opening (S1), the field ambience, the pack-up (S2), the break / groggy /
                 recovery (S3) and the meter notice (S5) (F:mboss/fieldgen/seq_f/**), called by the core's hooks.

The rig is the rig generator's (tools/build_mboss_fieldgen_rig.mjs: F:mboss/fieldgen/rig/** and the manifest); the
stand-in stub rig of the first stage was removed when the real rig was merged.

A pattern module defines PATTERNS (a list of api.Pattern) and emit(gen). emit writes only F:mboss/fieldgen/p/<key>/**
through gen.pw(key, name, lines): at least start, tick and cancel for every pattern it declares, optionally vis
(hz_vis events), pj_end (projectile events) and pause (the fight froze while it runs). The full contract between the
core and the pattern modules is the scratchpad file mb3/fg_contract.md.
"""

PATTERN_MODULES = ('cruise', 'field')
