# the point 21 b ahead is inside: is 26 b?
execute positioned ^ ^ ^26 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-26 run return run function rlk:mboss/butterfly/p/vacuum/edge/26_30
return run function rlk:mboss/butterfly/p/vacuum/edge/21_25
