# Start Q6 핏빛 연회 (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.
function rlk:boss/arlecchino/core/stop_move
scoreboard players set #pat kn 48
scoreboard players set #pt kn 0
scoreboard players set #done kn 0
scoreboard players operation #last2 kn = #last kn
scoreboard players set #last kn 16
scoreboard players operation #cd_Q6 kn = #clk kn
scoreboard players add #cd_Q6 kn 600
scoreboard players add #ai_nf kn 1
scoreboard players add #ai_nq kn 1
function rlk:boss/arlecchino/core/line/q6
function rlk:boss/arlecchino/hud/sub
function rlk:boss/arlecchino/p/q6/start
