# No line of sight (or out of range) at 27: the cage breaks, the screen clears, no pull and no swings.
execute at @e[tag=rlk_body,limit=1] run particle minecraft:block{block_state:"minecraft:black_concrete"} ~ ~1 ~ 0.4 0.8 0.4 0 20 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.7 0.6 0.3
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~ ~ 0.6 0.5 0.3
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p4cage]
kill @e[tag=rlk_mb_gd_p4scr]
kill @e[tag=rlk_mb_gd_p4scn]
