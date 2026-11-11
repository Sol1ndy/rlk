# MX pattern tick 21
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_mx16_15]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_mx16_17] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_mx16_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^-0.6 ^2.052 ^0.714 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_mx28,limit=1] ^-0.335 ^1.122 ^1.667
