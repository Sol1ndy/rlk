# the point 1 b ahead is inside: is 11 b?
execute positioned ^ ^ ^11 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-11 run return run function rlk:mboss/butterfly/p/vacuum/edge/11_20
return run function rlk:mboss/butterfly/p/vacuum/edge/1_10
