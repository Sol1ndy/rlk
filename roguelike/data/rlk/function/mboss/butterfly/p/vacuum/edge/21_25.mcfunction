# the point 21 b ahead is inside: is 23 b?
execute positioned ^ ^ ^23 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-23 run return run function rlk:mboss/butterfly/p/vacuum/edge/23_25
return run function rlk:mboss/butterfly/p/vacuum/edge/21_22
