# the point 23 b ahead is inside: is 24 b?
execute positioned ^ ^ ^24 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-24 run return run function rlk:mboss/butterfly/p/vacuum/edge/24_25
return run function rlk:mboss/butterfly/p/vacuum/edge/23_23
