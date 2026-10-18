# the point 21 b ahead is inside: is 22 b?
execute positioned ^ ^ ^22 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-22 run return run function rlk:mboss/butterfly/p/vacuum/edge/22_22
return run function rlk:mboss/butterfly/p/vacuum/edge/21_21
