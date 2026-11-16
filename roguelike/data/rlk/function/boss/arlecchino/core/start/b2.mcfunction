# Start B2 붉은 달의 낫 (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.
function rlk:boss/arlecchino/core/stop_move
scoreboard players set #pat kn 4
scoreboard players set #pt kn 0
scoreboard players set #done kn 0
scoreboard players operation #last2 kn = #last kn
scoreboard players set #last kn 2
scoreboard players operation #cd_B kn = #clk kn
scoreboard players add #cd_B kn 160
scoreboard players add #ai_nf kn 1
scoreboard players add #ai_nq kn 1
function rlk:boss/arlecchino/hud/sub
function rlk:boss/arlecchino/p/b2/start
