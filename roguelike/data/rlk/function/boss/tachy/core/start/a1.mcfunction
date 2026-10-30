# Start A1 돌진 베기 (@s = body; the AI, the rear / far rules, tests).
function rlk:boss/tachy/core/stop_move
scoreboard players set #pat tk 1
scoreboard players set #pt tk 0
scoreboard players set #done tk 0
scoreboard players set #core tk 0
scoreboard players operation #last2 tk = #last tk
scoreboard players set #last tk 1
scoreboard players add #kgap tk 1
execute if score #ai_fp tk matches 1 run scoreboard players set #t tk 120
execute if score #ai_fp tk matches 2 run scoreboard players set #t tk 120
execute if score #ai_fp tk matches 3 run scoreboard players set #t tk 96
scoreboard players operation #cd_a1 tk = #clk tk
scoreboard players operation #cd_a1 tk += #t tk
execute unless entity @s[tag=rlk_tk_mantle] run tag @s add rlk_tk_core
function rlk:boss/tachy/hud/sub
function rlk:boss/tachy/p/a1/start
