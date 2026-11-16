# Start Q5B 붉은 피의 연회 · 붉은 피의 사형 (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.
function rlk:boss/arlecchino/core/stop_move
scoreboard players set #pat kn 47
scoreboard players set #pt kn 0
scoreboard players set #done kn 0
scoreboard players operation #last2 kn = #last kn
scoreboard players set #last kn 15
scoreboard players add #ai_nf kn 1
scoreboard players set #ai_q5 kn 47
function rlk:boss/arlecchino/core/line/q5b
function rlk:boss/arlecchino/hud/sub
function rlk:boss/arlecchino/p/q5b/start
