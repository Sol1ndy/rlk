# Test 30: straight to P1b (HP at most the 70 % floor, E70 counted as done, floor 1).
execute unless function rlk:boss/arlecchino/core/force run return 0
scoreboard players set #fl kn 0
scoreboard players set #e70 kn 2
execute if score @s mhpC > #fl70 kn run scoreboard players operation @s mhpC = #fl70 kn
scoreboard players set #mbFloor mb 1
scoreboard players set #ph kn 3
function rlk:boss/arlecchino/ai/phase
function rlk:boss/arlecchino/ai/sched_f
function rlk:boss/arlecchino/core/looks
scoreboard players set #pat kn 0
function rlk:boss/arlecchino/ai/rec_start
function rlk:boss/arlecchino/hud/sub
