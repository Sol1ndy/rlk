#!/bin/bash
# S5 final: the numbers as generated (snapshot of wip/ar with the S5 changes), P1b and P2 (P1a hits unchanged: 'after').
cd "$(dirname "$0")"
SP='p1b:melee:walk:sword,p2:melee:walk:sword,p1b:melee:none:sword,p2:melee:none:sword,p1b:ranged:walk:bow,p2:ranged:walk:bow'
SPO='p1b:melee:walk:sword,p2:melee:walk:sword'
env -u KN_API -u KN_PMX -u KN_ORB python3 batch5.py final - $SP 4
env -u KN_API -u KN_PMX KN_ORB=1 python3 batch5.py final_orb - $SPO 4
echo PASS DONE
