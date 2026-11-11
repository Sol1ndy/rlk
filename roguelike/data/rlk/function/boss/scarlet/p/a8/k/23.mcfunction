# A8 pattern tick 23.
function rlk:boss/scarlet/g/cut/lock {s:30}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^0.679 ^1.776 ^-1.127 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b19] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4509f,1.5144f,-0.0545f],left_rotation:[-0.933f,0.25f,-0.067f,0.25f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.492 ^1.586 ^-0.197 run function rlk:boss/scarlet/core/sw/rib
