# Missile 10, clock 28: it reached the floor (its hazard strikes this tick).
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p4t9,limit=1] run function rlk:mboss/fieldgen/fx/snd/debris_land
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p4t9]
kill @s
