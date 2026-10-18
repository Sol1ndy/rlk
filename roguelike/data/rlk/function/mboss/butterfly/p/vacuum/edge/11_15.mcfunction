# the point 11 b ahead is inside: is 13 b?
execute positioned ^ ^ ^13 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-13 run return run function rlk:mboss/butterfly/p/vacuum/edge/13_15
return run function rlk:mboss/butterfly/p/vacuum/edge/11_12
