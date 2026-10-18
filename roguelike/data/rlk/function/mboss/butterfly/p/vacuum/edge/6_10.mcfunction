# the point 6 b ahead is inside: is 8 b?
execute positioned ^ ^ ^8 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-8 run return run function rlk:mboss/butterfly/p/vacuum/edge/8_10
return run function rlk:mboss/butterfly/p/vacuum/edge/6_7
