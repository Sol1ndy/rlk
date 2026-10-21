# One-shot interpolation, the tick after the summon (travelling cards: exactly the launch tick).
data modify entity @s transformation set from entity @s item.components."minecraft:custom_data".to
data modify entity @s interpolation_duration set from entity @s item.components."minecraft:custom_data".d
data modify entity @s start_interpolation set value 0
tag @s remove rlk_rd_fxa
