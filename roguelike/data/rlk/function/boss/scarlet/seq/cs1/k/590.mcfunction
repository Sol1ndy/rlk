# cs1: the timeline at #sq 590 (@s = the body).
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp_2]
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^-1.5 ^2 ^-2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqp","rlk_hr_sqp_2"],teleport_duration:1,view_range:2f}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_2,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"whole"}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_2,limit=1] run data merge entity @s {billboard:"center"}
function rlk:boss/scarlet/fx/snd/petal_drift
