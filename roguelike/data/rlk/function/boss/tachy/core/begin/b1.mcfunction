# Start B1 날개 가리기 2연격 (@s = body; the AI, the rear / far rules, tests).
function rlk:boss/tachy/core/stop_move
scoreboard players set #pat tk 2
scoreboard players set #pt tk 0
scoreboard players set #done tk 0
scoreboard players set #core tk 0
scoreboard players operation #last2 tk = #last tk
scoreboard players set #last tk 2
scoreboard players add #kgap tk 1
execute if score #ai_fp tk matches 1 run scoreboard players set #t tk 160
execute if score #ai_fp tk matches 2 run scoreboard players set #t tk 160
execute if score #ai_fp tk matches 3 run scoreboard players set #t tk 128
scoreboard players operation #cd_b1 tk = #clk tk
scoreboard players operation #cd_b1 tk += #t tk
function rlk:boss/tachy/hud/sub
function rlk:boss/tachy/p/b1/start
