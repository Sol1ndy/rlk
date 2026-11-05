# A9 pattern tick 28
execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ ~1.0 ~ run function rlk:boss/scarlet/fx/p/qi_cut with storage rlk:hr core.a9
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ ~1.0 ~ run function rlk:boss/scarlet/fx/p/qi_ring {r:40,c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/a9_cut
