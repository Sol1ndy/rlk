# the point 31 b ahead is inside: is 32 b?
execute positioned ^ ^ ^32 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-32 run return run function rlk:mboss/butterfly/p/vacuum/edge/32_32
return run function rlk:mboss/butterfly/p/vacuum/edge/31_31
