execute if entity @e[tag=rlk_dbtn,distance=..0.7] run tag @e[tag=rlk_dbtn,distance=..0.7,limit=1,sort=nearest] add rlk_dhover
execute if entity @e[tag=rlk_dbtn,distance=..0.7] run return 0
scoreboard players add #ray tmp 1
execute if score #ray tmp >= #rDitB view run return 0
execute positioned ^ ^ ^0.35 run function rlk:ditem/aim_btn_step
