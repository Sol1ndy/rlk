# A card with a second stage (tag rlk_rd_fxb) at 6 ticks of life left: its custom_data.to2 over d2 ticks.
data modify entity @s transformation set from entity @s item.components."minecraft:custom_data".to2
data modify entity @s interpolation_duration set from entity @s item.components."minecraft:custom_data".d2
data modify entity @s start_interpolation set value 0
tag @s remove rlk_rd_fxb
