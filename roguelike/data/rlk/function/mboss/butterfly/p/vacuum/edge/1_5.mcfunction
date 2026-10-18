# the point 1 b ahead is inside: is 3 b?
execute positioned ^ ^ ^3 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-3 run return run function rlk:mboss/butterfly/p/vacuum/edge/3_5
return run function rlk:mboss/butterfly/p/vacuum/edge/1_2
