# @s = a melee basic going to its socket (apSock): along the cradle (pushed out to r 3.4), then attacking.
execute if score @s apSock matches 0 if entity @e[type=minecraft:marker,tag=rlk_mb_ap_skm0,distance=..0.25] run return run function rlk:boss/apep/org/basic/at_sock
execute if score @s apSock matches 0 facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_skm0,limit=1] feet run function rlk:mboss/mv/step_flat {spd:0.12}
execute if score @s apSock matches 1 if entity @e[type=minecraft:marker,tag=rlk_mb_ap_skm1,distance=..0.25] run return run function rlk:boss/apep/org/basic/at_sock
execute if score @s apSock matches 1 facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_skm1,limit=1] feet run function rlk:mboss/mv/step_flat {spd:0.12}
execute if score @s apSock matches 2 if entity @e[type=minecraft:marker,tag=rlk_mb_ap_skm2,distance=..0.25] run return run function rlk:boss/apep/org/basic/at_sock
execute if score @s apSock matches 2 facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_skm2,limit=1] feet run function rlk:mboss/mv/step_flat {spd:0.12}
function rlk:boss/apep/org/basic/push_in
function rlk:boss/apep/om/face
