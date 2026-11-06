#!/bin/bash
# U1 sheet: front / side / back / 3-4 of P1 (wings off), P1 (wings open), P2, next to a 1.8 b stand-in (S:ar/renders/s2_U1.jpg)
cd /tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/ar/s2
rows=()
for spec in "p1off p1 {}" "p1open p1 {lV:1,lS:1,lF:10}" "p2 p2 {}" "p2open p2 {lS:1,lF:22}"; do
  set -- $spec
  node pose.mjs u1_$1 $2 "$3" > /dev/null
  ./r.sh u1_$1.jpg rlk:kn_dbg/p/u1_$1 rlk:kn_dbg/p/player -- --views front,right,back,az:45,12 --extent 3.4 --center 0.9 1.9 0 --aspect 0.75 --cols 4 --width 1280 \
    --title "$1: front / right side / back / 3-4 (stand-in: 1.8 b)"
  rows+=(u1_$1.jpg)
done
python3 - "${rows[@]}" <<'PY'
import sys
from PIL import Image
ims=[Image.open(f) for f in sys.argv[1:]]
w=640; ims=[i.resize((w, int(i.size[1]*w/i.size[0]))) for i in ims]
o=Image.new('RGB',(w,sum(i.size[1] for i in ims))); y=0
for i in ims: o.paste(i,(0,y)); y+=i.size[1]
o.save('../renders/s2_U1.jpg',quality=86)
print(o.size)
PY
rm -f "${rows[@]}"
