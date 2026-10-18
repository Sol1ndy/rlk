# vacuum clock 18
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p4g] run data merge entity @s {start_interpolation:0}
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p4g] run function rlk:mboss/butterfly/fx/prop/vblade
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p4g] remove rlk_mb_bf_p4g
execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^0.15 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
