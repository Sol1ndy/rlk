# the point 3 b ahead is inside: is 4 b?
execute positioned ^ ^ ^4 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-4 run return run function rlk:mboss/butterfly/p/vacuum/edge/4_5
return run function rlk:mboss/butterfly/p/vacuum/edge/3_3
