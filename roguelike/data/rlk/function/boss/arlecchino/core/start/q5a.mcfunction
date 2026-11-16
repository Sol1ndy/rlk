# Start Q5A 붉은 피의 연회 · 형벌의 핏값 (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.
function rlk:boss/arlecchino/core/stop_move
scoreboard players set #pat kn 46
scoreboard players set #pt kn 0
scoreboard players set #done kn 0
scoreboard players operation #last2 kn = #last kn
scoreboard players set #last kn 15
scoreboard players add #ai_nf kn 1
scoreboard players set #ai_q5 kn 46
function rlk:boss/arlecchino/core/line/q5a
function rlk:boss/arlecchino/hud/sub
function rlk:boss/arlecchino/p/q5a/start
