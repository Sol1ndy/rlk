# P3 tick (#apPT: burrow_in_p1 0-22, hidden, emerge_crown_p1 44-83, glow_slams 94-224); the live wheels first.
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p3w] at @s run function rlk:boss/apep/p/glow/wheel
execute if score #apPT mb matches 5..147 run return run function rlk:boss/apep/p/glow/kd/5_147
execute if score #apPT mb matches 148..225 run return run function rlk:boss/apep/p/glow/kd/148_225
