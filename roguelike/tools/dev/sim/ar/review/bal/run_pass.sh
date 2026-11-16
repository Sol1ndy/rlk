#!/bin/bash
# S5 balance pass: before (as merged on wip/ar) and after (the S5 numbers as an in-memory what-if), 3 seeds x 3600 t.
cd "$(dirname "$0")"
FINAL='{"WEIGHTS": {"Q1": {"p2": [25, 15, 0]}, "Q4": {"p2": [15, 25, 40]}, "Q6": {"p2": [15, 20, 25]}}, "COOLDOWN": {"Q1": 240}, "BOL_REHIT_PCT": 175, "P2_MUL": 100, "Q5B_PM": 300}'
SP='p1a:melee:walk:sword,p1b:melee:walk:sword,p2:melee:walk:sword,p1a:melee:none:sword,p1b:melee:none:sword,p2:melee:none:sword,p1a:ranged:walk:bow,p1b:ranged:walk:bow,p2:ranged:walk:bow'
SPO='p1a:melee:walk:sword,p1b:melee:walk:sword,p2:melee:walk:sword'
env -u KN_API -u KN_PMX -u KN_ORB python3 batch5.py before - $SP 3
env -u KN_API -u KN_PMX KN_ORB=1 python3 batch5.py before_orb - $SPO 3
env -u KN_ORB KN_API="$FINAL" KN_PMX=1 python3 batch5.py after - $SP 3
env KN_API="$FINAL" KN_PMX=1 KN_ORB=1 python3 batch5.py after_orb - $SPO 3
echo PASS DONE
