# G1 pattern tick 104
execute at @s run function rlk:boss/arlecchino/fx/snd/blast
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/thorns {r:240}
execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1] at @s run execute positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/blade_burst
function rlk:boss/arlecchino/rig/look/glow/normal
