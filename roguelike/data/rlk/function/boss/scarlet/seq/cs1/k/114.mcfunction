# cs1 at #sq 114 (@s = the body).
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp_1]
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^-0.7 ^2.05 ^1.0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqp","rlk_hr_sqp_1"],teleport_duration:1,view_range:2f}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] eyes run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"whole"}
function rlk:boss/scarlet/fx/snd/petal_drift
