# Start A5 사형장으로의 초대 (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.
function rlk:boss/arlecchino/core/stop_move
scoreboard players set #pat kn 2
scoreboard players set #pt kn 0
scoreboard players set #done kn 0
scoreboard players operation #last2 kn = #last kn
scoreboard players set #last kn 1
scoreboard players operation #cd_A kn = #clk kn
scoreboard players add #cd_A kn 60
scoreboard players add #ai_nf kn 1
scoreboard players add #ai_nq kn 1
scoreboard players operation #t kn = #clk kn
scoreboard players operation #t kn -= #lines kn
execute if score #t kn matches 80.. run function rlk:boss/arlecchino/core/line/a5
function rlk:boss/arlecchino/hud/sub
function rlk:boss/arlecchino/p/a5/start
