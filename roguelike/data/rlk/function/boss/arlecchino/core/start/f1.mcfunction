# Start F1 붉은 피의 연회 (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.
function rlk:boss/arlecchino/core/stop_move
scoreboard players set #pat kn 10
scoreboard players set #pt kn 0
scoreboard players set #done kn 0
scoreboard players operation #last2 kn = #last kn
scoreboard players set #last kn 8
scoreboard players add #ai_nq kn 1
function rlk:boss/arlecchino/core/line/f1
function rlk:boss/arlecchino/hud/sub
function rlk:boss/arlecchino/p/f1/start
