# The transition after a mantle (@s = body): M1 -> T1 날개 전개, M2 -> T2 심연; invulnerable throughout.
execute if score #ph tk matches 2 run scoreboard players set #ph tk 3
execute if score #ph tk matches 5 run scoreboard players set #ph tk 6
scoreboard players set #pat tk 54
scoreboard players set #pt tk 0
scoreboard players set #sq tk 0
scoreboard players set #sqdone tk 0
scoreboard players set #taken tk 100
tag @s add rlk_mb_inv
function rlk:boss/tachy/core/stop_move
execute if score #ph tk matches 3 run function rlk:boss/tachy/core/sq/t1/start
execute if score #ph tk matches 6 run function rlk:boss/tachy/core/sq/t2/start
function rlk:boss/tachy/hud/sub
