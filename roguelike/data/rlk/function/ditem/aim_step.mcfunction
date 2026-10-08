execute if entity @e[tag=rlk_ditem,distance=..1.4] run function rlk:ditem/aim_hit
execute if entity @e[tag=rlk_dinfo,distance=..2.2] run function rlk:ditem/aim_hit_info
execute if entity @e[tag=rlk_ditem,distance=..1.4] run return 0
execute if entity @e[tag=rlk_dinfo,distance=..2.2] run return 0
scoreboard players add #ray tmp 1
execute if score #ray tmp >= #rDit view run return 0
execute positioned ^ ^ ^0.5 run function rlk:ditem/aim_step
