# Q pattern tick 55
execute if score #q_hit hr matches 1 positioned as @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:mboss/mv/glide {t:4}
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/g_dive
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:30}
