# A10 pattern tick 24
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_20] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a10r0r20] remove rlk_hr_trg
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
