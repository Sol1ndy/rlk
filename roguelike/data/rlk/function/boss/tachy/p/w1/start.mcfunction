# W1 지상 장풍 (S4, p_air.py): pattern start (@s = the body, at it; #pt tk 0).
scoreboard players set #done tk 0
scoreboard players set #w1_s tk 0
scoreboard players set #w1_c tk 0
function rlk:mboss/mv/dist
execute if score #mbDist mb matches 120.. run return run function rlk:boss/tachy/p/w1/s/ch/go
function rlk:boss/tachy/p/w1/s/bl/go
