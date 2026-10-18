# the point 1 b ahead is inside: is 6 b?
execute positioned ^ ^ ^6 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-6 run return run function rlk:mboss/butterfly/p/vacuum/edge/6_10
return run function rlk:mboss/butterfly/p/vacuum/edge/1_5
