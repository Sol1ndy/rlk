# the point 16 b ahead is inside: is 18 b?
execute positioned ^ ^ ^18 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-18 run return run function rlk:mboss/butterfly/p/vacuum/edge/18_20
return run function rlk:mboss/butterfly/p/vacuum/edge/16_17
