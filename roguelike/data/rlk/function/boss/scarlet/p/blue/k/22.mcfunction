# BLUE pattern tick 22
execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ ~0.9 ~ run function rlk:boss/scarlet/fx/p/qi_cut with storage rlk:hr core.dash
execute at @s run function rlk:boss/scarlet/fx/snd/a2_hit
