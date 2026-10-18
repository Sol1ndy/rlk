# the point 34 b ahead is inside: is 35 b?
execute positioned ^ ^ ^35 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-35 run return run function rlk:mboss/butterfly/p/vacuum/edge/35_35
return run function rlk:mboss/butterfly/p/vacuum/edge/34_34
