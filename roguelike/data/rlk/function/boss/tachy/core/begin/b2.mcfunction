# Start B2 옆걸음 4연격 (@s = body; the AI, the rear / far rules, tests).
function rlk:boss/tachy/core/stop_move
scoreboard players set #pat tk 3
scoreboard players set #pt tk 0
scoreboard players set #done tk 0
scoreboard players set #core tk 0
scoreboard players operation #last2 tk = #last tk
scoreboard players set #last tk 3
scoreboard players add #kgap tk 1
execute if score #ai_fp tk matches 1 run scoreboard players set #t tk 140
execute if score #ai_fp tk matches 2 run scoreboard players set #t tk 140
execute if score #ai_fp tk matches 3 run scoreboard players set #t tk 112
scoreboard players operation #cd_b2 tk = #clk tk
scoreboard players operation #cd_b2 tk += #t tk
function rlk:boss/tachy/hud/sub
function rlk:boss/tachy/p/b2/start
