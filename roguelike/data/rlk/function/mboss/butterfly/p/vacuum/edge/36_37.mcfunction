# the point 36 b ahead is inside: is 37 b?
execute positioned ^ ^ ^37 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-37 run return run function rlk:mboss/butterfly/p/vacuum/edge/37_37
return run function rlk:mboss/butterfly/p/vacuum/edge/36_36
