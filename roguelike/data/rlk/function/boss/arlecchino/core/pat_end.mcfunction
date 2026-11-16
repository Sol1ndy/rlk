# The pattern set #done (@s = body): the window closed, the looks back, the schedules, the recovery.
function rlk:boss/arlecchino/core/win_off
scoreboard players set #done kn 0
scoreboard players operation #dec kn = #pat kn
scoreboard players set #pat kn 0
kill @e[type=minecraft:marker,tag=rlk_kn_lock]
scoreboard players set #pt kn 0
function rlk:boss/arlecchino/core/looks_rest
function rlk:boss/arlecchino/core/ground
execute if score #dec kn matches 20 run function rlk:boss/arlecchino/core/e70_end
execute if score #dec kn matches 10 run function rlk:boss/arlecchino/ai/resched_f
execute if score #dec kn matches 46 run function rlk:boss/arlecchino/ai/resched_q5
execute if score #dec kn matches 47 run function rlk:boss/arlecchino/ai/resched_q5
execute if score #dec kn matches 41 run function rlk:boss/arlecchino/core/q0_end
function rlk:boss/arlecchino/ai/rec_start
function rlk:boss/arlecchino/hud/sub
