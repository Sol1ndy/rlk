# D4 pattern tick 37
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_d434] ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d434_33] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_d434_35] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/blade_mid
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_d444] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_d444,limit=1] ^0.113 ^3.132 ^0.722
