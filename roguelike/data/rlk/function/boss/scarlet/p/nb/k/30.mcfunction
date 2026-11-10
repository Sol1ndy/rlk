# NB pattern tick 30
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~30 0 positioned ~ ~0.6 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.5 0.3 4 0 40 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~30 0 positioned ~ ~0.6 ~ run particle minecraft:dust{color:[1.0,0.95,0.98],scale:1.0} ~ ~ ~ 0.3 0.2 3 0 12 force @a[tag=player]
execute at @s run function rlk:boss/scarlet/fx/snd/g_sweep
