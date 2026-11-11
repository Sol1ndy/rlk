# A8 pattern tick 81.
function rlk:boss/scarlet/g/cut/lock {s:88}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^-0.223 ^2.891 ^0.366 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b76] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.1381f,0.6231f,0.2899f],left_rotation:[-0.6865f,-0.6214f,0.2296f,0.2998f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_77] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_79] remove rlk_hr_trr
execute at @s rotated as @s rotated ~ 0 positioned ^-0.252 ^0.644 ^0.172 run function rlk:boss/scarlet/core/sw/rib
