# A8 pattern tick 96.
function rlk:boss/scarlet/g/cut/aim {s:108}
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~75 0 positioned ^ ^ ^4.4 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b76] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4744f,1.5986f,0.0231f],left_rotation:[-0.8881f,-0.3679f,0.1055f,0.2547f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_88]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_90] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
