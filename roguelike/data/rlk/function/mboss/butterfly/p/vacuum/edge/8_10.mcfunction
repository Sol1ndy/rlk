# the point 8 b ahead is inside: is 9 b?
execute positioned ^ ^ ^9 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-9 run return run function rlk:mboss/butterfly/p/vacuum/edge/9_10
return run function rlk:mboss/butterfly/p/vacuum/edge/8_8
