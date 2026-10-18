# the point 1 b ahead is inside: is 2 b?
execute positioned ^ ^ ^2 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-2 run return run function rlk:mboss/butterfly/p/vacuum/edge/2_2
return run function rlk:mboss/butterfly/p/vacuum/edge/1_1
