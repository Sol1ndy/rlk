#!/bin/bash
# The 아를레키노 suites (scratchpad ar/tests) against one datapack root (read only: variant trees go to tmp/ here).
#   ./run_all.sh <worktree>/roguelike [tag]     outputs out/<tag>_<suite>.txt; exit 1 on any failure
# S1: test_cm_ar.py (FN-1, FN-3, routing, music) and test_arena_fl.py (the fl_ruins theme). Later stages add theirs.
# (11-03: every path quoted, so a checkout path with a space cannot split the cleanup rm -rf below)
H=$(dirname "$(realpath "$0")")
DP=$(realpath "${1:?usage: run_all.sh <datapack root> [tag]}")
TAG=${2:-ar}
mkdir -p "$H/out" "$H/tmp"
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
rc=0
for t in test_cm_ar test_arena_fl test_kit; do
  [ -f "$H/$t.py" ] || continue
  t0=$(date +%s)
  python3 "$H/$t.py" "$DP" > "$H/out/${TAG}_$t.txt" 2>&1; r=$?
  n=$(grep -c '^ok ' "$H/out/${TAG}_$t.txt"); f=$(grep -c '^FAIL' "$H/out/${TAG}_$t.txt")
  echo "$([ $r -eq 0 ] && echo 'ok  ' || echo 'FAIL') $t: $n ok, $f failed ($(( $(date +%s) - t0 )) s)"
  [ $r -ne 0 ] && { grep '^FAIL' "$H/out/${TAG}_$t.txt" | head; tail -3 "$H/out/${TAG}_$t.txt"; rc=1; }
done
rm -rf "$H"/tmp/cm_* 2>/dev/null; rmdir "$H/tmp" 2>/dev/null
exit $rc
