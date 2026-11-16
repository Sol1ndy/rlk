# F1 pattern tick 196
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/blast {r:260}
execute at @s run function rlk:boss/arlecchino/fx/snd/blast
execute at @s run function rlk:boss/arlecchino/fx/snd/cracks
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/decal/cracks {r:260}
function rlk:boss/arlecchino/rig/look/glow/normal
