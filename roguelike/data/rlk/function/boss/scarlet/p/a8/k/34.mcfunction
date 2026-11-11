# A8 pattern tick 34.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c30]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c30_28]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c30_30] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c30_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/g/cut/aim {s:48}
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~-60 0 positioned ^ ^ ^3.6 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
