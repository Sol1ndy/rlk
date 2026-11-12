# The transition is over (or a reload / test finishes it; @s = body): P2 (T1) or P3 (T2, the HP floor off).
tag @s remove rlk_mb_inv
execute if score #ph tk matches 3 run scoreboard players set #ph tk 4
execute if score #ph tk matches 6 run scoreboard players set #mbFloor mb 0
execute if score #ph tk matches 6 run scoreboard players set #ph tk 7
scoreboard players set #pat tk 0
scoreboard players set #sq tk 0
scoreboard players set #sqdone tk 0
scoreboard players set #aut tk 20
function rlk:boss/tachy/ai/phase
function rlk:boss/tachy/core/looks
function rlk:boss/tachy/ai/rec_start
scoreboard players set #rec tk 10
function rlk:boss/tachy/hud/sub
