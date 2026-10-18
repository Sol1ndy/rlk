# the point 9 b ahead is inside: is 10 b?
execute positioned ^ ^ ^10 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-10 run return run function rlk:mboss/butterfly/p/vacuum/edge/10_10
return run function rlk:mboss/butterfly/p/vacuum/edge/9_9
