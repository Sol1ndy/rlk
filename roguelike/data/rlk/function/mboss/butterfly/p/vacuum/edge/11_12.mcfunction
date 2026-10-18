# the point 11 b ahead is inside: is 12 b?
execute positioned ^ ^ ^12 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-12 run return run function rlk:mboss/butterfly/p/vacuum/edge/12_12
return run function rlk:mboss/butterfly/p/vacuum/edge/11_11
