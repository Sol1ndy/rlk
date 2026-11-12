# Missile 4, clock 15: the dive onto rlk_mb_fg_p4t3 (+0.6 b), one interpolated teleport of 13 t.
data merge entity @s {teleport_duration:13}
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_fg_p4t3,limit=1] run tp @s ~ ~0.6 ~
