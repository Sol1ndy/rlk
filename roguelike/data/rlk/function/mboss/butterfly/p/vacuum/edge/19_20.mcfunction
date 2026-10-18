# the point 19 b ahead is inside: is 20 b?
execute positioned ^ ^ ^20 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-20 run return run function rlk:mboss/butterfly/p/vacuum/edge/20_20
return run function rlk:mboss/butterfly/p/vacuum/edge/19_19
