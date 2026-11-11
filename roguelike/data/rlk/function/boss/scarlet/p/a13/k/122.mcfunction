# A13 pattern tick 122.
function rlk:boss/scarlet/rig/play/g_x
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/glide {t:2}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b101] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4746f,1.5095f,0.0154f],left_rotation:[-0.8835f,-0.366f,0.1119f,0.2701f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_114]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_116] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
