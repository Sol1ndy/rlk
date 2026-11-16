# The B3 crater (decor, footage v6 10.55-11.15 s): the kit crater prop at the floor cut of the arena
# centre, fixed UUID 0x81 (Rig decision change 3); re-made by reload / resume; gone at the surfacing.
kill @e[type=minecraft:item_display,tag=rlk_mb_az_p23c]
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.03 ~ run summon minecraft:item_display ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,129],Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p23c"],Rotation:[0f,0f],billboard:"fixed"}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p23c] run function rlk:boss/azhdaha/fx/prop/crater
