# Start Q2 불꽃이 타오르는 낫 (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.
function rlk:boss/arlecchino/core/stop_move
scoreboard players set #pat kn 43
scoreboard players set #pt kn 0
scoreboard players set #done kn 0
scoreboard players operation #last2 kn = #last kn
scoreboard players set #last kn 12
scoreboard players operation #cd_Q2 kn = #clk kn
scoreboard players add #cd_Q2 kn 160
scoreboard players add #ai_nf kn 1
scoreboard players add #ai_nq kn 1
function rlk:boss/arlecchino/hud/sub
function rlk:boss/arlecchino/p/q2/start
