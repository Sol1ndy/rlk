# G1 pattern tick 62
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:boss/arlecchino/fx/snd/cross_hit
execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1] at @s run execute positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/blade_burst
kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1]
