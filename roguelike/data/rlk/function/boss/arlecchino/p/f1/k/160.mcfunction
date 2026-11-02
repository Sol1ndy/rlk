# F1 pattern tick 160
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.2 ~ run function rlk:boss/arlecchino/fx/p/threads {r:260}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/p/thorns {r:260}
execute at @s run function rlk:boss/arlecchino/fx/snd/threads
