tag @s remove rlk_pk_hl
execute if entity @s[type=minecraft:item_display] run data merge entity @s {start_interpolation:0,interpolation_duration:2,Glowing:0b}
execute if entity @s[type=minecraft:item_display] run data modify entity @s transformation.scale set value [0.6f,0.6f,0.6f]
execute if entity @s[type=minecraft:text_display] run data modify entity @s background set value 1344282672
