#!/usr/bin/env python3
"""야타용왕 (Azhdaha) chapter-1 boss module generator.

    python3 tools/build_mboss_azhdaha.py

Registry entry: tools/mboss_registry.json id "azhdaha", n 10, kind chapter, arena az_cavern (cm.md 2). Writes
F:mboss/azhdaha/** except the rig's AZ:rig/** (tools/build_mboss_azhdaha_rig.mjs, wip/az-rig) and the kit's owned paths
(tools/build_mboss_az_fx.py, the manifest "owned" list), and deletes stale files only in what it owns, so the
generators run in any order and twice without a change.

Generator order (README "야타용왕"): build_mboss_core.py -> build_mboss_arena.py -> build_cboss_rooms.py -> (the rig,
resource pack) -> build_mboss_az_fx.py -> this -> check_mboss_pack.py. The core reads the committed stub manifest
tools/mboss_azhdaha/stub_rig_manifest.json (written here), so a commit that changes it also commits the regenerated
core outputs (cm.md 1.2).

The generator is the package tools/mboss_azhdaha/: api.py (shared helpers and the manifest merge), core.py (hooks, AI
host, slots, services, HUD, tests), ai.py, brand.py, h_core.py, stub_rig.py (the stand-in rig) and one file per
pattern group (geo_a.py, geo_b.py, leg.py, tail.py) plus trans.py / seq.py (the transitions, intro and death).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_azhdaha import core  # noqa: E402

core.build()
