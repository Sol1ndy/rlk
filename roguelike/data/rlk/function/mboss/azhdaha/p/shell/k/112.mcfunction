# shell #azPT 112
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s4,limit=1] run data merge entity @s {teleport_duration:8}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s4,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_p44l4,limit=1] run tp @s ~ ~0.6 ~
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p44s4,limit=1] run function rlk:mboss/azhdaha/fx/snd/shell_dive
function rlk:mboss/mv/turn {max:2}
