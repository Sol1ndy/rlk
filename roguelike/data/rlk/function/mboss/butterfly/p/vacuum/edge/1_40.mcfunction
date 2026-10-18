# the point 1 b ahead is inside: is 21 b?
execute positioned ^ ^ ^21 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-21 run return run function rlk:mboss/butterfly/p/vacuum/edge/21_40
return run function rlk:mboss/butterfly/p/vacuum/edge/1_20
