# Q pattern tick 95
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run function rlk:boss/scarlet/fx/p/sky_pillar {r:24}
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:boss/scarlet/fx/snd/sky_pillar
