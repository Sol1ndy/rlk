# the point 11 b ahead is inside: is 16 b?
execute positioned ^ ^ ^16 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-16 run return run function rlk:mboss/butterfly/p/vacuum/edge/16_20
return run function rlk:mboss/butterfly/p/vacuum/edge/11_15
