#!/bin/bash
# r.sh <out.jpg> <apply fn...> -- [extra renderer args]   (Arlecchino rig debug renders; dbg dp in S:ar/s2/dbg)
S=/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad
out=$1; shift
apply=()
while [ $# -gt 0 ] && [ "$1" != "--" ]; do apply+=("$1"); shift; done
[ "$1" == "--" ] && shift
python3 -I $S/az/understand/rigtech_render.py --dp $S/ar/s2/dbg --rp $S/ar/rp_s2 \
  --spawn rlk:boss/arlecchino/rig/spawn --apply "${apply[@]}" --light mc -q -o $out "$@" 2>&1 | grep -iE "error|traceback|missing" | head -5
