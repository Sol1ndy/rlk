#!/bin/bash
# strip.sh <clip> <step> [view] [extent] [cx cy cz] [out] : one strip of a clip (dbg frames kn_dbg/<clip>/<t>)
S=/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad
M=$S/ar/wt_s2/roguelike/tools/arlecchino_rig_manifest.json
c=$1; st=${2:-4}; v=${3:-az:20,8}; ext=${4:-2.3}; cx=${5:-0}; cy=${6:-1.5}; cz=${7:-0}; out=${8:-$S/ar/s2/st_$c.jpg}
L=$(python3 -c "import json;print(json.load(open('$M'))['clips']['$c']['len'])")
d=$c; [ -d $S/ar/s2/dbg/data/rlk/function/kn_dbg/${c}_p1 ] && d=${c}_p1
cd $S/ar/s2 && ./r.sh $out "rlk:kn_dbg/$d/{t}" -- --strip 0..$L:$st --views $v --extent $ext --center $cx $cy $cz --cols ${COLS:-6} --width ${W:-1200} --title "$c ($L t) every $st t, $v"
