# A13 pattern tick 121.
function rlk:boss/scarlet/g/cut/lock {s:128}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^0.073 ^3.127 ^-0.021 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b101] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4744f,1.5986f,0.0231f],left_rotation:[-0.8881f,-0.3679f,0.1055f,0.2547f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_113]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_115] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
