# {sel,p,d,look}: every clone part matching sel eases to pose p over d ticks, in look dark|glow.
$execute as @e[type=minecraft:item_display,tag=rlk_rd_clp,$(sel)] run data modify entity @s transformation set from entity @s item.components."minecraft:custom_data".P.$(p)
$execute as @e[type=minecraft:item_display,tag=rlk_rd_clp,$(sel)] run data merge entity @s {start_interpolation:0,interpolation_duration:$(d)}
$execute as @e[type=minecraft:item_display,tag=rlk_rd_clp,$(sel)] run data modify entity @s item.components."minecraft:item_model" set from entity @s item.components."minecraft:custom_data".$(look)
