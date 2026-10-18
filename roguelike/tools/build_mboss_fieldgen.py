#!/usr/bin/env python3
"""Field generator (실험성 역장 발생 장치, nameplate 브레게 프로토타입) mid-boss module generator.

    python3 tools/build_mboss_fieldgen.py

Registry entry: tools/mboss_registry.json id "fieldgen", n 3. Writes F:mboss/fieldgen/** except
F:mboss/fieldgen/rig/** (the rig generator's, branch wip/fg-rig) and F:mboss/fieldgen/fx/** (the fx kit's, branch
wip/fg-fx), and deletes stale files only in what it owns, so the generators run in any order and twice without a
change.

Generator order (README "등록 · 모듈"): build_mboss_core.py (whenever the registry changes) -> build_mboss_arena.py ->
build_mboss_proto.py -> (the rig generators, resource pack) -> build_mboss_guardian.py -> build_mboss_bf_fx.py ->
build_mboss_butterfly.py -> this -> check_mboss_pack.py.

The generator is the package tools/mboss_fieldgen/: core.py (hooks, the state machine, the break meter, low gravity,
HUD, tests) plus one file per pattern group (cruise.py C1-C6, field.py F1-F2 and the waves), so the pattern authors
work in parallel without touching shared files. While the real rig manifest (tools/mboss_fieldgen_rig_manifest.json)
does not exist, the module calls the removable stub rig F:mboss/fieldgen/rig_stub/ (tools/mboss_fieldgen/stub_rig.py).
The core <-> pattern contract is in tools/mboss_fieldgen/api.py and the scratchpad fg_contract.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_fieldgen import core  # noqa: E402

core.build()
