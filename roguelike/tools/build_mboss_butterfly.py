#!/usr/bin/env python3
"""Moonlit Illusion Butterfly (달빛 환영 나비, title 달빛의 화신) mid-boss module generator.

    python3 tools/build_mboss_butterfly.py

Registry entry: tools/mboss_registry.json id "butterfly", n 2. Writes F:mboss/butterfly/** except
F:mboss/butterfly/rig/** (that belongs to the rig generator) and deletes stale files there. Run
tools/build_mboss_core.py first whenever the registry changes, then this, then tools/check_mboss_pack.py.

The generator is the package tools/mboss_butterfly/: core.py (hooks, forms, AI, debuff, heal orbs, entrance,
death, HUD, tests) plus one file per pattern group (human.py H1-H4, wing.py B1-B5), so the pattern authors work
in parallel without touching shared files. While the real rig manifest (tools/mboss_butterfly_rig_manifest.json)
does not exist, the module calls the removable stub rig F:mboss/butterfly/rig_stub/ (tools/mboss_butterfly/
stub_rig.py). The core <-> pattern contract is in tools/mboss_butterfly/api.py and the scratchpad bf_contract.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_butterfly import core  # noqa: E402

core.build()
