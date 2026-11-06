#!/bin/bash
# b.sh [extra builder args]: build the Arlecchino rig into the S2 worktree + RP copy, debug dp S:ar/s2/dbg
S=/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad
cd $S/ar/wt_s2/roguelike && node tools/build_arlecchino_rig.mjs --resourcepack $S/ar/rp_s2 --debug-dp $S/ar/s2/dbg "$@" 2>&1 | tail -30
