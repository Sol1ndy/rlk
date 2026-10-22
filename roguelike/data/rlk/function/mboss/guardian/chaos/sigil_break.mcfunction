execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_sigil] at @s run particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~ ~ 0.15 0.15 0.15 0 4 force @a[tag=player]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_sigil]
