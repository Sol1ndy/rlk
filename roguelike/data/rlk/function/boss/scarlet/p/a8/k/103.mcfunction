# A8 pattern tick 103.
function rlk:boss/scarlet/rig/play/g_x
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/glide {t:2}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b79] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4757f,1.5082f,0.0175f],left_rotation:[-0.8835f,-0.366f,0.1119f,0.2701f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
