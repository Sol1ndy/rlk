# Start C3 붉은 핵 연속기 (@s = body; the AI, the rear / far rules, tests).
function rlk:boss/tachy/core/stop_move
scoreboard players set #pat tk 7
scoreboard players set #pt tk 0
scoreboard players set #done tk 0
scoreboard players set #core tk 0
scoreboard players operation #last2 tk = #last tk
scoreboard players set #last tk 7
scoreboard players add #kgap tk 1
execute if score #ai_fp tk matches 1 run scoreboard players set #t tk 200
execute if score #ai_fp tk matches 2 run scoreboard players set #t tk 200
execute if score #ai_fp tk matches 3 run scoreboard players set #t tk 160
scoreboard players operation #cd_c3 tk = #clk tk
scoreboard players operation #cd_c3 tk += #t tk
execute unless entity @s[tag=rlk_tk_mantle] run tag @s add rlk_tk_core
function rlk:boss/tachy/hud/sub
function rlk:boss/tachy/p/c3/start
