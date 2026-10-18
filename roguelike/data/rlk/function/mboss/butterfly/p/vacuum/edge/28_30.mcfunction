# the point 28 b ahead is inside: is 29 b?
execute positioned ^ ^ ^29 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-29 run return run function rlk:mboss/butterfly/p/vacuum/edge/29_30
return run function rlk:mboss/butterfly/p/vacuum/edge/28_28
