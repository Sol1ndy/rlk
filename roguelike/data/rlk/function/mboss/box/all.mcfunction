# From room/tick while #mbBoxOn mb is 1 (drop_all sets it, every box alive keeps it): fall and idle shimmer.
scoreboard players set #mbBoxOn mb 0
execute as @e[type=minecraft:item_display,tag=rlk_mb_box] at @s run function rlk:mboss/box/tick
