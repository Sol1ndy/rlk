# MX pattern tick 14
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^1.6 if function rlk:mboss/mv/ok run function rlk:mboss/mv/glide {t:2}
execute at @s run function rlk:boss/scarlet/fx/snd/g_dash
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:90}
