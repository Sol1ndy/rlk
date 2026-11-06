"""홍련 (Scarlet), the special boss reached through a room rift (plan S:hr/PLAN.md; contract S:hr/contract.md): module
generator package. Ownership (contract §1, PLAN §9.1):

api         the frozen D0 contract (identity, registry + arena constants, DMG / HITS / gauntlet scripts, floors, pips,
            switches, AI tables, keys, lines, names, rig / kit / sequence / shield / event call names, Writer + Pattern +
            Service, cut / disc builders, ownership, test ids)                          (D0 = lead; changes by request)
stub_rig_manifest.json   the D0 part / clip table read until S2a's tools/scarlet_rig_manifest.json lands   (D0)
core ai shield p1 s3lib  hooks, phase machine, floors, invulnerability, counters, down window, shield / pips / judge,
                         ult/fatal, AI, A1-A10, HUD wiring, look request, decor props, pause / reload / cleanup  (S3)
reward                   the event logic ev/** + the FN-b reward hook (PLAN §7.3)                              (S3)
p_ghost                  R1-R3, the gauntlets A8 / A13, the ghost helpers g/** (cut builder, reappear, discs)    (S4)
seq                      intro, cs1, sq1, repel, lead_down, lead_stand, ending, event bodies                   (S2b)
The top-level generator is tools/build_mboss_scarlet.py (S3); the rig (S2a, tools/build_scarlet_rig.mjs) and the kit
(S1K, tools/build_mboss_hr_fx.py) write their own trees rig/** and fx/**.
"""
PATTERN_MODULES = ('p1', 'p_ghost')
SERVICE_MODULES = ('seq', 'reward')
