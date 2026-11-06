# E1 pattern tick 70
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:mboss/mv/glide {t:6}
execute at @s run function rlk:boss/arlecchino/fx/snd/dive
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/dive_streak {len:60}
