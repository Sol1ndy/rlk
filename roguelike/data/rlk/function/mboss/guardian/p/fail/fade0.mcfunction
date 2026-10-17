# Spear 1 dissolves upward into cubes.
execute at @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s0,limit=1] run particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~-4 ~ 0.4 3 0.4 0 24 force @a[tag=player]
kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s0]
kill @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0]
