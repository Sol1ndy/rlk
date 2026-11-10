#!/bin/bash
# regen_all.sh [<roguelike dir>] [--mobs]: run every registry-reading Python generator (datapack side; kits with --skip-rp)
# in the documented order, then the pack checker. Afterwards `git status` must list only the files your change owns, and a
# second run must change nothing (release gate "regenerate twice -> identical").
#   --mobs   also run build_ch2_mobs.py and build_ch3_mobs.py (they write shared hook lines; deterministic, any order)
# The resource-pack side (node rig builders, kits with --resourcepack <RP>, bossbar, minimap, Raiden) is NOT run here:
# README.md chapter 0 ("빌드 순서") lists those commands.
# Each generator's output goes to one log file, shown only on failure. Log dir: $RLK_REGEN_LOGDIR (default: mktemp in $TMPDIR).
DP=$(cd "$(dirname "$0")/../.." && pwd); MOBS=0
for a in "$@"; do case $a in --mobs) MOBS=1;; *) DP=$a;; esac; done
cd "$DP" || exit 2
if [ -n "$RLK_REGEN_LOGDIR" ]; then mkdir -p "$RLK_REGEN_LOGDIR"; LOG=$(mktemp "$RLK_REGEN_LOGDIR/regen.XXXXXX.log")
else LOG=$(mktemp "${TMPDIR:-/tmp}/rlk_regen.XXXXXX.log"); fi
fail=0
run() { echo "== $*"; if ! timeout 900 python3 "$@" > "$LOG" 2>&1; then echo "FAILED: $*"; tail -20 "$LOG"; fail=1; fi; }
run tools/build_mboss_core.py
run tools/build_mboss_arena.py
run tools/build_cboss_rooms.py
run tools/build_mboss_proto.py
run tools/build_mboss_cproto.py
run tools/build_mboss_spproto.py
run tools/build_mboss_guardian.py
run tools/build_mboss_butterfly.py
run tools/build_mboss_fieldgen.py
run tools/build_mboss_az_fx.py --skip-rp
run tools/build_mboss_azhdaha.py
run tools/build_mboss_ap_fx.py --skip-rp
run tools/build_mboss_apep.py
run tools/build_rift.py
run tools/build_mboss_tk_fx.py --skip-rp
run tools/build_mboss_tachy.py
[ -f tools/build_mboss_kn_fx.py ] && run tools/build_mboss_kn_fx.py --skip-rp
[ -f tools/build_mboss_arlecchino.py ] && run tools/build_mboss_arlecchino.py
[ -f tools/build_mboss_hr_fx.py ] && run tools/build_mboss_hr_fx.py --skip-rp
[ -f tools/build_mboss_scarlet.py ] && run tools/build_mboss_scarlet.py
if [ $MOBS = 1 ]; then run tools/build_ch2_mobs.py; run tools/build_ch3_mobs.py; fi
# balance gauge (combat overhaul lane B): rlk:bal/** (datapack only here; the font with --resourcepack, README 0-4)
run tools/build_balance.py
run tools/check_mboss_pack.py
tail -1 "$LOG"; rm -f "$LOG"
echo "== done (failures: $fail)"; exit $fail
