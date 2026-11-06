#!/usr/bin/env python3
"""Corrupted Guardian (파수꾼・타락) mid-boss module generator.

    python3 tools/build_mboss_guardian.py

Registry entry: tools/mboss_registry.json id "guardian", n 1. Writes F:mboss/guardian/** except
F:mboss/guardian/rig/** (that belongs to tools/build_mboss_guardian_rig.mjs) and deletes stale
files there. Run tools/build_mboss_core.py first whenever the registry changes, then this, then
tools/check_mboss_pack.py.

The generator is the package tools/mboss_guardian/: core.py (hooks, AI, guard, chaos, groggy, HUD,
tests) plus one file per pattern group (p12.py P1/P2, p34.py P3/P4, p56.py P5/P6 sweeps/fail
spears), so pattern authors work in parallel without touching shared files. The core <-> pattern
contract is in tools/mboss_guardian/api.py and README "파수꾼・타락 모듈".
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_guardian import core  # noqa: E402

core.build()
