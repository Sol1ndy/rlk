# F1 pattern tick 110
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/decal/flood {r:260,t:50}
execute at @s run function rlk:boss/arlecchino/fx/snd/flood
