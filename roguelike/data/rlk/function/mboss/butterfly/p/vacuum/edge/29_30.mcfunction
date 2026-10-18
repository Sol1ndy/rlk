# the point 29 b ahead is inside: is 30 b?
execute positioned ^ ^ ^30 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-30 run return run function rlk:mboss/butterfly/p/vacuum/edge/30_30
return run function rlk:mboss/butterfly/p/vacuum/edge/29_29
