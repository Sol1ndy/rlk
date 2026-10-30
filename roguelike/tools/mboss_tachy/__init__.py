"""타키 (Tachy), the special boss reached through a room rift (plan S:tk/PLAN.md; contract S:tk/contract.md): module
generator package. Ownership (contract §1):

api         the frozen D0 contract (ids, registry + arena constants, DMG / HITS / EL tables, clips, parts, looks, rig
            and kit call names, scores / tags / storage, pattern + writer interface, test ids)       (D0; changes by request)
stub_rig_manifest.json   the D0 clip / part table the core reads until S2's tools/tachy_rig_manifest.json lands (D0)
core ai elem p_melee     hooks, phases, floors, G1-G3, AI, A1 B1 B2 B3 C1-C3, HUD wiring, tests               (S3)
s3lib                    S3 helpers + the pattern builder PB (p_melee, elem, core; S4 imports it)          (S3)
p_air p_mantle           K, W1, W2, L; mantle feathers + nova                                                 (S4)
seq                      intro, death, T1 wing unfurl, T2 abyss bodies                                       (S2)
The top-level generator is tools/build_mboss_tachy.py (S3).
"""
PATTERN_MODULES = ('p_melee', 'p_air', 'p_mantle')
SERVICE_MODULES = ('seq',)
