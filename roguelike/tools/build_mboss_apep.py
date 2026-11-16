#!/usr/bin/env python3
"""아펩의 오아시스 파수꾼 (Apep) chapter-3 boss module generator.

    python3 tools/build_mboss_apep.py

Registry entry: tools/mboss_registry.json id "apep", n 11, kind chapter, ch [3], arena ap_oasis (n 2) (cm.md 2; the
scratchpad ap/ap_contract.md 0.3.6). Writes F:boss/apep/** except the rig's AP:rig/** (tools/build_mboss_apep_rig.mjs,
wip/ap-rig), the org generator's AP:om/** (wip/ap-org) and the kit's owned paths (tools/build_mboss_ap_fx.py, the
manifest "owned" list), and deletes stale files only in what it owns, so the generators run in any order and twice
without a change.

Generator order: build_mboss_core.py -> build_mboss_arena.py -> build_cboss_rooms.py -> (the rig, the org models, the
resource pack) -> build_mboss_ap_fx.py -> this -> check_mboss_pack.py. The core reads the committed stub manifest
tools/mboss_apep/stub_rig_manifest.json (written here), so a commit that changes it also commits the regenerated core
outputs (cm.md 1.2).

The generator is the package tools/mboss_apep/: api.py (the stable contract), core.py (hooks, phases, slot, services,
HUD, tests), ai.py, stub_rig.py / stub_rig_rt.py (the rig stand-in, dropped at AP-I2; the stub org was dropped at AP-I1), the pattern modules p1.py, p3.py,
aftermath.py and the service modules seq.py, revival.py, org.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_apep import core  # noqa: E402

core.build()
