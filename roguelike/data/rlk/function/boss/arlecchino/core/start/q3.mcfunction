# Start Q3 붉은 죽음의 무도회 (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.
function rlk:boss/arlecchino/core/stop_move
scoreboard players set #pat kn 44
scoreboard players set #pt kn 0
scoreboard players set #done kn 0
scoreboard players operation #last2 kn = #last kn
scoreboard players set #last kn 13
scoreboard players operation #cd_Q3 kn = #clk kn
scoreboard players add #cd_Q3 kn 120
scoreboard players add #ai_nf kn 1
scoreboard players add #ai_nq kn 1
function rlk:boss/arlecchino/hud/sub
function rlk:boss/arlecchino/p/q3/start
