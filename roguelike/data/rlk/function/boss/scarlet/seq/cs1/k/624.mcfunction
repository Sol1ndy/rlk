# cs1: the timeline at #sq 624 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"cut"}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] run data merge entity @s {billboard:"center"}
function rlk:boss/scarlet/fx/snd/petal_cut
