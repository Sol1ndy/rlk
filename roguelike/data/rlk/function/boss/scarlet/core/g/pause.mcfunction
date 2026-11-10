# A gauntlet paused (@s = body): cancelled now; what resume does (#grs). F1: the judged A8 fail -> P2 (4, HR-01);
# a lethal gauntlet past its last counting cut with pips left -> the fail pending (5, HR-07); a test's forced fail
# (#pipoff) ends here (HR-06). Already cancelled (a /reload while the pause lasts: core/re/g): the first pause's
# #grs stands (the shield and the clock are gone by now).
execute if score #pat hr matches 0 run return 0
scoreboard players set #grs hr 1
execute if score #gres hr matches 1 run scoreboard players set #grs hr 3
execute if score #gres hr matches 2 if score #gk hr matches 2 run scoreboard players set #grs hr 2
execute if score #gres hr matches 2 if score #gk hr matches 1 run scoreboard players set #grs hr 4
execute if score #gres hr matches 0 if score #gk hr matches 2 if score #gau hr matches 1.. if score #pt hr matches 219.. run scoreboard players set #grs hr 5
scoreboard players set #pipoff hr 0
function rlk:boss/scarlet/core/cancel_d
scoreboard players set #pat hr 0
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
function rlk:boss/scarlet/shield/off
function rlk:boss/scarlet/fx/hud/warn {on:0}
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/core/ground
function rlk:boss/scarlet/rig/look/form/normal
tag @s remove rlk_hr_ghost
