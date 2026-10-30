# shells #apq33T 14
function rlk:mboss/mv/turn {max:3}
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p33","rlk_mb_ap_p33q"]}
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_p33q,tag=!rlk_mb_ap_p33x] apT 0
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p33q] add rlk_mb_ap_p33x
scoreboard players add @e[type=minecraft:marker,tag=rlk_mb_ap_p33q] apT 1
function rlk:boss/apep/p/shells/ring_step
execute at @s rotated as @s positioned ^0 ^9.39 ^-0.48 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p33","rlk_mb_ap_p33o"],teleport_duration:2,item:{id:"minecraft:paper",count:1}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33o] run function rlk:boss/apep/fx/prop/charge_ball
execute at @s run function rlk:boss/apep/fx/snd/q3_charge
