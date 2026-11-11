# A8 pattern tick 192.
function rlk:boss/scarlet/rig/look/blade/pink
function rlk:boss/scarlet/rig/anchor/blade_tip
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/g_glow
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b154] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.1201f,1.3792f,0.3808f],left_rotation:[-0.5792f,-0.0616f,0.4056f,0.7044f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_184]
