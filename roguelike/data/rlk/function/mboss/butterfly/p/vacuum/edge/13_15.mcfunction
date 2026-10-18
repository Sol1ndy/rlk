# the point 13 b ahead is inside: is 14 b?
execute positioned ^ ^ ^14 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-14 run return run function rlk:mboss/butterfly/p/vacuum/edge/14_15
return run function rlk:mboss/butterfly/p/vacuum/edge/13_13
