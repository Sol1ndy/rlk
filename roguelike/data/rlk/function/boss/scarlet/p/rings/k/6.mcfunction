# RINGS pattern tick 6
function rlk:mboss/mv/turn {max:10}
execute at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute at @s run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_rings14] ~ ~ ~ ~ 0
execute at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_rings14,limit=1] ^1.561 ^1.06 ^0.964
