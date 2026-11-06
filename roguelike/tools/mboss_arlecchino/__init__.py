"""아를레키노 (Arlecchino, "The Knave"), the chapter-4 boss (plan S:ar/PLAN.md; contract S:ar/contract.md): module
generator package. Ownership (contract §1):

api         the frozen D0 contract (ids, registry + arena constants, DMG / HITS tables, the FN-1 bond option names, bond /
            break numbers, AI tables, clips, parts, looks, anchors, rig and kit call names, dialog lines, scores / tags /
            storage, pattern + writer interface, test ids)                                     (D0; changes by request)
stub_rig_manifest.json   the D0 clip / part table read until S2's tools/arlecchino_rig_manifest.json lands   (D0)
core ai bond p1 s3lib    hooks, phases, floors, E70, Bond of Life / 선혈의 충격 / break, AI, phase-1 patterns (S3)
p2                       phase-2 patterns Q0-Q6                                                          (S4)
seq                      intro, t_p2 transition, death bodies                                           (S2)
The top-level generator is tools/build_mboss_arlecchino.py (S3).
"""
PATTERN_MODULES = ('p1', 'p2')
SERVICE_MODULES = ('seq',)
