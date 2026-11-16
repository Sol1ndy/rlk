# Q6 stage main tick 160
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:mboss/mv/glide {t:8}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/dive_streak {len:120}
execute at @s run function rlk:boss/arlecchino/fx/snd/fall_dive
