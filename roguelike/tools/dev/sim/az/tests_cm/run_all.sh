#!/bin/bash
# Every check of the chapter-boss mode (AZ-CM, S1-CM) against one datapack root (read-only: nothing in the tree changes).
#
#   ./run_all.sh <worktree>/roguelike [tag]          RP=<unpacked resource pack> ./run_all.sh ...  (+ the RP builds twice)
#
# (shape of scratchpad mb3/tests/run_all.sh; cm.md 15.5)
#  1. the chapter-mode suites (this folder): test_chapter.py (routing, entrance, gate, spawn, kill economy, abort, lose,
#     pools, test commands, music, cp_test looks, cleanup paths, Raiden smoke), test_px.py (hit proxies), test_fw_az.py
#     (the Azhdaha / Apep framework helpers), test_fw_ap.py (the AP-FW gaps, cm.md 22; skipped with rc 0 on a tree without
#     AP-FW); harness lib/cmsim.py on vendored copies of the S1-HARN sims (README.md);
#     test_m0diff.py (the four mid-bosses against the release 22ba247 archive by behaviour, same seed: traces, logs, end states,
#     commands per tick; the boss bar line; CM fix round IDENTITY-1/2/3)
#  2. the M0 suites, unchanged and run from their own folders: scratchpad mb3/tests (field generator, cruise / field
#     patterns, e2e, framework options, e2e butterfly), mb3/tests/bf_base (the release butterfly suites), mb3/fxtests
#     (the fg kit), mb2/tests (butterfly suites of the release line), mb2/fxtests (the bf kit), mb/int_tests (framework /
#     Guardian)
#  3. gen_check.py (generator order and idempotency incl. arena, build_cboss_rooms, cproto; RP adds the kits' and the
#     boss bar's RP builds twice) and ident.py (Guardian / butterfly / fieldgen / proto outputs, the plaza, the sources
#     and the engine files against the release 22ba247 = M0 039b911 + the 10-20 release; the content of the shared
#     edits pinned in baseline/shared_edits.diff)
#  4. validators: check_refs, check_macro (run from the root), check_nbtpath, tools/check_mboss_pack.py, lint_mc,
#     compared with baseline/ by vcheck.py (only new findings fail)
# Suites run 3 at a time (JOBS=n to change). One line per step; outputs in out/<tag>_<step>.txt; exit 1 on any failure.
# Temporary files (tempfile, the variant trees of test_chapter) go to tmp/ here; no byte code is written anywhere.
S=/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad
H=$(dirname "$(realpath "$0")")
DP=$(realpath "${1:?usage: run_all.sh <datapack root> [tag]}")
TAG=${2:-all}
O=$H/out
JOBS=${JOBS:-3}
mkdir -p $O $H/tmp
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$H/tmp
[ -f "$DP/data/rlk/function/mboss/cb/route.mcfunction" ] || { echo "not a datapack root with the chapter mode: $DP"; exit 2; }

steps=()          # name|command
for t in test_m0diff test_chapter test_px test_fw_az test_fw_ap; do [ -f $H/$t.py ] && steps+=("cm_$t|python3 $H/$t.py $DP"); done
for t in test_fieldgen pat_cruise pat_field test_e2e_fieldgen test_fwopts test_e2e_butterfly; do steps+=("mb3_$t|python3 $S/mb3/tests/$t.py $DP"); done
for t in test_butterfly test_pjx test_human test_fx_engine; do steps+=("mb3bf_$t|python3 $S/mb3/tests/bf_base/$t.py $DP"); done
steps+=("mb3fx_test_fg_fx|python3 $S/mb3/fxtests/test_fg_fx.py $DP")
for t in ${MB2_TESTS-test_butterfly test_e2e_butterfly test_pjx test_human test_fixes}; do steps+=("mb2_$t|python3 $S/mb2/tests/$t.py $DP"); done
steps+=("mb2fx_test_fx_engine|python3 $S/mb2/fxtests/test_fx_engine.py $DP")
for t in test_guardian test_e2e_guardian test_p12 test_p34 test_p56 test_life test_hz test_mv test_pj test_roll test_box; do
  steps+=("int_$t|python3 $S/mb/int_tests/$t.py $DP")
done
if [ -n "$RP" ]; then steps+=("gen_check|python3 $H/gen_check.py $DP --rp $(realpath $RP)"); else steps+=("gen_check|python3 $H/gen_check.py $DP"); fi
steps+=("ident|python3 $H/ident.py $DP")
steps+=("v_refs|python3 $S/check_refs.py $DP")
steps+=("v_macro|cd $DP && python3 $S/check_macro.py $DP")
steps+=("v_nbt|python3 $S/check_nbtpath.py $DP/data")
steps+=("v_pack|cd $DP && python3 tools/check_mboss_pack.py")
steps+=("v_lint|python3 $S/mb/lint_mc.py $DP")

run_step() {      # name command...
  local name=$1; shift
  timeout 2400 bash -c "$*" > $O/${TAG}_$name.txt 2>&1
  echo $? > $O/${TAG}_$name.rc
}
t0=$(date +%s)
running=0
for st in "${steps[@]}"; do
  run_step "${st%%|*}" "${st#*|}" &
  running=$((running + 1))
  if [ $running -ge $JOBS ]; then wait -n; running=$((running - 1)); fi
done
wait

rc=0
for st in "${steps[@]}"; do
  name=${st%%|*}
  r=$(cat $O/${TAG}_$name.rc)
  case $name in
    v_refs|v_macro|v_lint|v_nbt|v_pack)
      [ $r -ne 0 ] && [ $name != v_lint ] && { echo "FAIL $name: the validator exited $r"; rc=1; continue; }
      line=$(python3 $H/vcheck.py ${name#v_} $O/${TAG}_$name.txt); r=$?
      echo "$line" | head -1; [ $r -ne 0 ] && echo "$line" | tail -n +2 | head -20 ;;
    *)
      echo "$([ $r -eq 0 ] && echo 'ok  ' || echo 'FAIL') $name rc=$r  $(grep -v '^\s*$' $O/${TAG}_$name.txt | tail -n 1 | cut -c1-150)" ;;
  esac
  [ $r -ne 0 ] && rc=1
done
rmdir $H/tmp 2>/dev/null
echo "run_all: $([ $rc -eq 0 ] && echo 'ALL GREEN' || echo 'FAILURES') in $(( $(date +%s) - t0 )) s ($DP, outputs $O/${TAG}_*.txt)"
exit $rc
