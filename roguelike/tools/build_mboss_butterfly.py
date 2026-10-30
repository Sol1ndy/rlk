#!/usr/bin/env python3
"""Moonlit Illusion Butterfly (달빛 환영 나비, title 달빛의 화신) mid-boss module generator.

    python3 tools/build_mboss_butterfly.py

Registry entry: tools/mboss_registry.json id "butterfly", n 2. Writes F:mboss/butterfly/** except
F:mboss/butterfly/rig/** (the rig generator's) and the fx kit's paths (tools/build_mboss_bf_fx.py: fx/{card,cardx,
look,clear,uninstall}, fx/{e,p,tele,snd,hud,prop,test}/**; tools/mboss_bf_fx_manifest.json "owned"), and deletes stale
files only in what it owns, so the generators run in any order and twice without a change.

Generator order (README "등록 · 모듈"): build_mboss_core.py (whenever the registry changes) -> build_mboss_arena.py ->
build_mboss_proto.py -> (the rig generators, resource pack) -> build_mboss_guardian.py -> build_mboss_bf_fx.py
(--resourcepack <RP> or --skip-rp) -> this -> check_mboss_pack.py. The effect engine is the fx kit (api.K, Gen.fx /
snd / kcard / tele_* / kprop / khud); this generator imports its Python call builders only.

The generator is the package tools/mboss_butterfly/: core.py (hooks, forms, AI, debuff, heal orbs, entrance,
death, HUD, tests) plus one file per pattern group (human.py H1-H4, wing.py B1-B5), so the pattern authors work
in parallel without touching shared files. Clips, events, fx anchors and props come from the rig manifest
tools/mboss_butterfly_rig_manifest.json (node tools/build_mboss_butterfly_rig.mjs, which runs before this one). The
core <-> pattern contract is in tools/mboss_butterfly/api.py and the scratchpad bf_contract.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_butterfly import core  # noqa: E402

core.build()
