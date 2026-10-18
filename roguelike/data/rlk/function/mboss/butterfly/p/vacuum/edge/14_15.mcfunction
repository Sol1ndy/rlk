# the point 14 b ahead is inside: is 15 b?
execute positioned ^ ^ ^15 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-15 run return run function rlk:mboss/butterfly/p/vacuum/edge/15_15
return run function rlk:mboss/butterfly/p/vacuum/edge/14_14
