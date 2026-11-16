#!/bin/bash
# pv.sh <name> <form> '<json>' [views] [extent] [cx cy cz]: solve a pose and render it (S:ar/s2/pv_<name>.jpg)
cd /tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/ar/s2
node pose.mjs "$1" "$2" "$3" || exit 1
V=${4:-front,right,az:45,12,top}
./r.sh pv_$1.jpg rlk:kn_dbg/p/$1 -- --views $V --extent ${5:-2.4} --center ${6:-0} ${7:-1.4} ${8:-0} --cols 4 --width 1280 --title "$1"
