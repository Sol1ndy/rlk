# cs1: the timeline at #sq 647 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^1 ^0.92 ^1.15 run tp @s ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"cut"}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] run data merge entity @s {billboard:"center"}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] run data merge entity @s {transformation:{scale:[0.95f,0.95f,0.95f]}}
function rlk:boss/scarlet/fx/snd/petal_cut
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^1 ^0.92 ^1.15 run function rlk:boss/scarlet/fx/p/glint {c:5}
