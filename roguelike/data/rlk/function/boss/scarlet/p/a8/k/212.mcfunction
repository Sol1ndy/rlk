# A8 pattern tick 212.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b203] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0667f,2.1841f,0.389f],left_rotation:[-0.8292f,0.004f,-0.0075f,0.5589f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_204]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_206] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_210] remove rlk_hr_trr
