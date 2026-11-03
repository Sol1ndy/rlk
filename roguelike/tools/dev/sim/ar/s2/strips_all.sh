#!/bin/bash
# strips_all.sh [clip ...]: S:ar/renders/s2_clips/<clip>.jpg, every 2 t, 640 px wide (view from her front-right, 20 deg)
S=/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad
M=$S/ar/wt_s2/roguelike/tools/arlecchino_rig_manifest.json
cd $S/ar/s2; mkdir -p ../renders/s2_clips
clips=("$@"); [ ${#clips[@]} -eq 0 ] && clips=($(python3 -c "import json;print(' '.join(json.load(open('$M'))['clips']))"))
for c in "${clips[@]}"; do
  L=$(python3 -c "import json;print(json.load(open('$M'))['clips']['$c']['len'])")
  f=$(python3 -c "import json;print(json.load(open('$M'))['clips']['$c']['form'] or 'any')")
  ext=2.6; cen="0 1.7 0"
  case $c in t_p2) ext=4.6; cen="0 4.0 0";; q6|q0_hover|q0_dive|q4_up|q4_shot|q4_land|q5a|q5b|q1|q2|q3|idle2|walk2|strafe2_*|stun2|death|f1|e70) ext=3.4; cen="0 2.2 0";; esac
  d=$c; [ -d dbg/data/rlk/function/kn_dbg/${c}_p1 ] && d=${c}_p1
  ./r.sh ../renders/s2_clips/$c.jpg "rlk:kn_dbg/$d/{t}" -- --strip 0..$L:2 --views az:20,8 --extent $ext --center $cen --cols 10 --width 640 --title "$c ($L t, form $f): every 2 t"
done
