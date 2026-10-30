# @s = body (slam 2, t164): two homing thorn wheels (#pjNoDodge 1, sphere hr 1.0, 15 % each)
# on the carpet front (r 3.0) at +-12 deg of the player's bearing: 0.75 b/t for 6 t, then
# 0.5 b/t, steering from 2 t (pj/steer {max:8}), life 22 t; wheel 1 shares the carpet's group.
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~-12 0 positioned ^ ^1.05 ^3 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p3","rlk_mb_ap_p3w","rlk_mb_ap_p3wn"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p3wn] run function rlk:boss/apep/fx/prop/thorn_wheel_homing
scoreboard players set #pjEl mb 7
scoreboard players set #pjNoDodge mb 1
scoreboard players operation #pjGrp mb = #apq3G mb
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p3wn] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] feet rotated ~180 0 run function rlk:mboss/pj/launch {spd:7,life:22,dmg:15,hr:10}
tag @e[type=minecraft:item_display,tag=rlk_mb_ap_p3wn] remove rlk_mb_ap_p3wn
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~12 0 positioned ^ ^1.05 ^3 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p3","rlk_mb_ap_p3w","rlk_mb_ap_p3wn"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p3wn] run function rlk:boss/apep/fx/prop/thorn_wheel_homing
scoreboard players set #pjEl mb 7
scoreboard players set #pjNoDodge mb 1
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p3wn] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] feet rotated ~180 0 run function rlk:mboss/pj/launch {spd:7,life:22,dmg:15,hr:10}
tag @e[type=minecraft:item_display,tag=rlk_mb_ap_p3wn] remove rlk_mb_ap_p3wn
