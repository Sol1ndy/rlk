# E70 is over (@s = body): P1b with the <= 70 % kit, the F schedule starts.
tag @s remove rlk_mb_inv
scoreboard players set #mbFloor mb 1
scoreboard players set #e70 kn 2
scoreboard players set #ph kn 3
function rlk:boss/arlecchino/ai/phase
function rlk:boss/arlecchino/ai/sched_f
