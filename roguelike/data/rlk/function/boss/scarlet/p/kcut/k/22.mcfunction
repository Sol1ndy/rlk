# KCUT pattern tick 22
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated ~-90 0 positioned ^6 ^0.9 ^ run function rlk:boss/scarlet/fx/p/qi_line {len:120}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated ~-35 0 positioned ^6 ^0.9 ^ run function rlk:boss/scarlet/fx/p/qi_line {len:120}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated ~-145 0 positioned ^6 ^0.9 ^ run function rlk:boss/scarlet/fx/p/qi_line {len:120}
execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ ~0.8 ~ run function rlk:boss/scarlet/fx/p/qi_cut with storage rlk:hr core.dash
execute at @s run function rlk:boss/scarlet/fx/snd/a9_cut
