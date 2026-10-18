# the point 18 b ahead is inside: is 19 b?
execute positioned ^ ^ ^19 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-19 run return run function rlk:mboss/butterfly/p/vacuum/edge/19_20
return run function rlk:mboss/butterfly/p/vacuum/edge/18_18
