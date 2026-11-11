# NB pattern tick 40
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s rotated ~0 0 positioned ~ ~0.6 ~ run function rlk:boss/scarlet/fx/p/qi_beam {len:160}
execute at @s run function rlk:boss/scarlet/fx/snd/g_sweep
execute at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:6}
