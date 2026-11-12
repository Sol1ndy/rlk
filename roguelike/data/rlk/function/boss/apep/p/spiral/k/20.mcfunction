# spiral #apq35T 20
function rlk:mboss/mv/turn {max:3}
execute at @s rotated as @s positioned ^2.5 ^9.5 ^0.5 as @e[type=minecraft:item_display,tag=rlk_mb_ap_p35o,scores={apL=1}] run tp @s ~ ~ ~
execute at @s rotated as @s positioned ^0 ^7.95 ^0.6 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p35","rlk_mb_ap_p35o","rlk_mb_ap_p35n"],teleport_duration:5,item:{id:"minecraft:paper",count:1}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p35n] run function rlk:boss/apep/fx/prop/seed_orb
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_ap_p35n] apL 7
tag @e[type=minecraft:item_display,tag=rlk_mb_ap_p35n] remove rlk_mb_ap_p35n
execute at @s run function rlk:boss/apep/fx/snd/q5_orb
