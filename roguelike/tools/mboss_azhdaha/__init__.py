"""야타용왕 (Azhdaha), the chapter-1 boss (plan S:az/plan.md; contracts S:az/contract/*.md): module generator package.

api      shared constants, the manifest merge, the Gen / Pattern / TL helpers for pattern authors (s2.md 2-5)
core     hooks, AI host, slots, services, fields, orbs, after / addons, HUD, tests (S1-MOD)
ai       zone sampling, candidates, weighted pick (S1-MOD)
brand    the Pyro / Cryo / Electro brand, shards (S1-MOD)
h_core   pure geometry helpers and the timing-correct pattern stubs (S1-MOD)
stub_rig the stand-in rig and the v1 stub manifest (manifest.md 8; S1-MOD)
geo_a geo_b leg tail   pattern modules (S2-A / S2-B / S2-L / S2-T; empty stubs until those stages land)
trans seq              transition services and the intro / death (S2-S; working stubs by S1-MOD)
"""
PATTERN_MODULES = ('geo_a', 'geo_b', 'leg', 'tail', 'trans', 'seq')
