# the point 16 b ahead is inside: is 17 b?
execute positioned ^ ^ ^17 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-17 run return run function rlk:mboss/butterfly/p/vacuum/edge/17_17
return run function rlk:mboss/butterfly/p/vacuum/edge/16_16
