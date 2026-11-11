# RINGS pattern tick 48
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_42]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_44] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_rings44_46] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute if score #ph hr matches 7 run tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute if score #ph hr matches 7 rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_rings54,limit=1] ^1.254 ^1.065 ^1.375
execute if score #ph hr matches 1 unless score #ultq hr matches 1 run function rlk:boss/scarlet/ai/tail
