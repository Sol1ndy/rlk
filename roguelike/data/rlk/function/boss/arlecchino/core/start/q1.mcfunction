# Start Q1 사형장으로의 초대 (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.
function rlk:boss/arlecchino/core/stop_move
scoreboard players set #pat kn 42
scoreboard players set #pt kn 0
scoreboard players set #done kn 0
scoreboard players operation #last2 kn = #last kn
scoreboard players set #last kn 11
scoreboard players operation #cd_Q1 kn = #clk kn
scoreboard players add #cd_Q1 kn 240
scoreboard players add #ai_nf kn 1
scoreboard players add #ai_nq kn 1
function rlk:boss/arlecchino/hud/sub
function rlk:boss/arlecchino/p/q1/start
